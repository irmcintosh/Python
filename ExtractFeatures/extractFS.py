import arcpy
import requests
import json
import time
import logging
from typing import List, Tuple, Dict
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlencode

# Setup logging
logging.basicConfig(filename='feature_extraction.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Setup
arcpy.env.overwriteOutput = True
baseURL = "Rest End Point"  # Replace with your actual URL
fields = "*"  # Fields to retrieve
outdata = "output location"  # Replace with your desired output location


def get_max_record_count(base_url: str) -> int:
    urlstring = f"{base_url}?f=json"
    try:
        response = requests.get(urlstring)
        response.raise_for_status()
        js = response.json()
        max_record_count = int(js["maxRecordCount"])
        logging.info(f"Record extract limit: {max_record_count}")
        return max_record_count
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching max record count: {e}")
        exit()


def get_object_ids(base_url: str) -> Tuple[str, List[int]]:
    urlstring = f"{base_url}/query?where=1=1&returnIdsOnly=true&f=json"
    try:
        response = requests.get(urlstring)
        response.raise_for_status()
        js = response.json()
        id_field = js["objectIdFieldName"]
        id_list = js["objectIds"]
        id_list.sort()
        logging.info(f"Number of target records: {len(id_list)}")
        return id_field, id_list
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching object IDs: {e}")
        exit()


def fetch_features(url: str) -> Dict:
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching features from {url}: {e}")
        return {}


def gather_features(base_url: str, id_field: str, id_list: List[int], max_rc: int) -> List[arcpy.FeatureSet]:
    num_rec = len(id_list)
    feature_sets = {}
    urls = []

    for i in range(0, num_rec, max_rc):
        to_rec = i + (max_rc - 1)
        if to_rec > num_rec - 1:
            to_rec = num_rec - 1
        from_id = id_list[i]
        to_id = id_list[to_rec]
        where = f"{id_field} >= {from_id} and {id_field} <= {to_id}"
        params = {
            "where": where,
            "returnGeometry": "true",
            "outFields": fields,
            "f": "json"
        }
        query_string = urlencode(params)
        urlstring = f"{base_url}/query?{query_string}"
        urls.append(urlstring)

    # Fetch data in parallel
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(fetch_features, urls))

    # Load features into FeatureSets
    for i, result in enumerate(results):
        if result:
            feature_set = arcpy.FeatureSet()
            feature_set.load(result)
            feature_sets[i] = feature_set

    return list(feature_sets.values())


def save_features(feature_sets: List[arcpy.FeatureSet], output_location: str):
    try:
        arcpy.Merge_management(feature_sets, output_location)
        logging.info("Features saved successfully.")
    except arcpy.ExecuteError as e:
        logging.error(f"Error saving features: {e}")
        exit()


def main():
    max_record_count = get_max_record_count(baseURL)
    id_field, id_list = get_object_ids(baseURL)
    feature_sets = gather_features(baseURL, id_field, id_list, max_record_count)
    save_features(feature_sets, outdata)
    logging.info("Done!")


if __name__ == "__main__":
    main()
