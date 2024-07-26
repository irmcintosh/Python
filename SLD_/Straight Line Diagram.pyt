import arcpy, os
import arcpy.conversion
import arcpy.da
import arcpy.management
from time import sleep

arcpy.env.overwriteOutput = True

def _getCatalogPath(input_feature_layer) -> dict:
    """
        Private function the return feature data source
        path
    """
    des = arcpy.Describe(input_feature_layer)
    des_dict = {'dir': des.path, 'base': des.name, "full": os.path.join(des.path,des.name)}
    return des_dict

def _get_spatial_reference(feature_class) -> dict:
    """
        Private function get's the spatial reference
        and returns a dictionary
    """
    try:
        # Describe the feature class to get its properties
        desc = arcpy.Describe(feature_class)
        
        # Get the spatial reference from the description
        spatial_ref = desc.spatialReference
        
        # # Print spatial reference details
        # print(f"Spatial Reference for {feature_class}:")
        # print(f"Name: {spatial_ref.name}")
        # print(f"Factory Code (WKID): {spatial_ref.factoryCode}")
        # print(f"Projection: {spatial_ref.projectionName}")
        # print(f"Datum: {spatial_ref.datumName}")
        # print(f"Coordinate System Type: {spatial_ref.type}")
        
        return {'sr':spatial_ref, 'mt': spatial_ref.MTolerance, 'mr':spatial_ref.MResolution}

    except Exception as e:
        print(f"Error reading spatial reference: {e}")
        return None
    
def _get_current_project_folder():
    """
        Private function returns the current project
        workspace
    """
    # Get the current ArcGIS Pro project
    aprx = arcpy.mp.ArcGISProject("CURRENT")

    # Get the file path of the project
    project_path = aprx.filePath

    # Extract the folder path from the project path
    project_folder = arcpy.os.path.dirname(project_path)

    return project_folder

def _copy_domain(source_fc, target_fc, workspace):
    # Get the domains from the source feature class
    source_domains = arcpy.da.ListDomains(source_fc)

    # Dictionary to map domain names to their properties
    domain_dict = {domain.name: domain for domain in source_domains}

    # Get the fields from the source feature class
    source_fields = arcpy.ListFields(source_fc)

    # For each field in the source feature class
    for field in source_fields:
        if field.domain:
            domain_name = field.domain
            domain = domain_dict[domain_name]

            # Check if the domain already exists in the target feature class
            target_domains = arcpy.da.ListDomains(target_fc)
            target_domain_names = [d.name for d in target_domains]

            # If the domain doesn't exist, create it
            if domain_name not in target_domain_names:
                if domain.domainType == 'CodedValue':
                    arcpy.management.CreateDomain(arcpy.env.workspace, domain_name, domain.description, domain.type, 'CODED')
                    for code, value in domain.codedValues.items():
                        arcpy.management.AddCodedValueToDomain(arcpy.env.workspace, domain_name, code, value)
                elif domain.domainType == 'Range':
                    arcpy.management.CreateDomain(arcpy.env.workspace, domain_name, domain.description, domain.type, 'RANGE')
                    arcpy.management.SetValueForRangeDomain(arcpy.env.workspace, domain_name, domain.range[0], domain.range[1])

            # Assign the domain to the corresponding field in the target feature class
            arcpy.management.AssignDomainToField(target_fc, field.name, domain_name)


    
def _find_shape(words) -> list:
    import re
    """
        Private function that search's for SHAPE field
        and returns those matches as a list
    """
    pattern = re.compile(r"\bSHAPE\b", re.IGNORECASE)
    return [word for word in words if pattern.search(word)] 
  
def _find_SL(words) -> list:
    import re
    """
        Private function that search's for Shape__Length
        field and returns those matches as a list
    """
    pattern = re.compile(r"\Shape__Length\b", re.IGNORECASE)
    return [word for word in words if pattern.search(word)]  

def _extract_alphanumeric(text):
    import re
    # Define the regex pattern to match only alphanumeric characters
    pattern = re.compile(r'[a-zA-Z0-9]+')
    
    # Find all matches in the input text
    matches = pattern.findall(text)
    
    # Join the matches to form a single string
    result = ''.join(matches)
    
    return result

class Toolbox:
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "StraightLineDiagram"
        self.alias = "SLD"

        # List of tool classes associated with this toolbox
        self.tools = [GenerateHorizontalRoute, GenerateHorizontalRouteEvent]


class GenerateHorizontalRoute:
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "1) Generate Horizontal Routes"
        self.description = "This GP tool generates horizontal linear features"

    def getParameterInfo(self):
        """Define the tool parameters."""

        # Route Feature Layer
        params0 = arcpy.Parameter()
        params0.name = 'input_lrs_route'
        params0.displayName = 'Input LRS Route Feature'
        params0.parameterType = 'Required'
        params0.direction = 'Input'
        params0.datatype = 'GPFeatureLayer'
        params0.filter.list = ['POLYLINE']
        params0.displayOrder = 1

        params1 = arcpy.Parameter()
        params1.name = 'input_field_fromMeas'
        params1.displayName = 'From-Measure Field'
        params1.parameterType = 'Optional'
        params1.direction = 'Input'
        params1.datatype = 'Field'
        params1.parameterDependencies =[params0.name]
        params1.displayOrder = 4

        params2 = arcpy.Parameter()
        params2.name = 'input_field_toMeas'
        params2.displayName = 'To-Measure Field'
        params2.parameterType = 'Optional'
        params2.direction = 'Input'
        params2.datatype = 'Field'
        params2.parameterDependencies =[params0.name]
        params2.displayOrder = 5

        # Output Feature Layer
        params3 = arcpy.Parameter()
        params3.name = 'output_sld_name'
        params3.displayName = 'Output GDB SLD Name'
        params3.parameterType = 'Required'
        params3.direction = 'Input'
        params3.datatype = 'GPString'
        params3.displayOrder = 6

        params4 = arcpy.Parameter()
        params4.name = 'input_bool_measSource'
        params4.displayName = 'Use measure values from data source'
        params4.parameterType = 'Required'
        params4.direction = 'Input'
        params4.datatype = 'Boolean'
        params4.value = False
        params4.displayOrder = 3

        params5 = arcpy.Parameter()
        params5.name = 'input_route_id'
        params5.displayName = 'Route Identifier Field '
        params5.parameterType = 'Required'
        params5.direction = 'Input'
        params5.datatype = 'Field'
        params5.parameterDependencies = [params0.name]
        params5.displayOrder = 2

        
        
        return [params0,
                params1,
                params2,
                params3,
                params4,
                params5]

    def isLicensed(self):
        """Set whether the tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""

        if bool(parameters[4].value):
            parameters[1].enabled = False
            parameters[2].enabled = False
        else:
            parameters[1].enabled = True
            parameters[2].enabled = True

        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter. This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        # Get te workspace and set over
        projectWS = arcpy.env.workspace
        
        # Set variables
        input_routeLayer = parameters[0].valueAsText
        input_froMeas = parameters[1].valueAsText
        input_toMeas = parameters[2].valueAsText
        outputName = parameters[3].valueAsText
        input_bool_measS = parameters[4].value
        input_route_rid = parameters[5].valueAsText

        # list to hold data that needs to be deleted
        deleteList = [] 

        # Create a copy of the Input Rotue Layer
        routeLayerPath = _getCatalogPath(input_routeLayer)
        routeLayerCopy = arcpy.CreateScratchName("SLDRoute", 
                                                 'FeatureClass',
                                                 projectWS)
        # Get spatial and M information
        sr = _get_spatial_reference(input_routeLayer)   
        arcpy.env.MResolution = sr['mr']
        arcpy.env.MTolerance = sr['mt']
        arcpy.management.CreateFeatureclass(projectWS, 
                                            os.path.basename(routeLayerCopy),
                                            'POLYLINE', 
                                            input_routeLayer, 
                                            'ENABLED', 
                                            'DISABLED',
                                            sr['sr'],
                                            out_alias='SLD Route Temp')
        arcpy.ResetEnvironments()
        deleteList.append(routeLayerCopy)

        # Read the Route layer to Create the Horizontal Routes
        # Get the field names and add the Shape field so that
        # the can be inserted
        fields = [f.name for f in arcpy.ListFields(input_routeLayer) ]
                
        # Remove the Shape/Shape Length field because it causes issues
        fieldSL = _find_SL(fields)
        fieldS = _find_shape(fields)
        if bool(fieldSL):
            fields.pop(fields.index(fieldSL[0]))
        if bool(fieldS):
            fields.pop(fields.index(fieldS[0]))
        fields.insert(0, 'SHAPE@')

        # Use SearchCursor to loop through each Row to insert
        # into the temporary feature
        totalRecords = int(arcpy.management.GetCount(input_routeLayer)[0]  )
        arcpy.SetProgressor('step', "Processing Routes...", 0, totalRecords, 1)  
        arcpy.AddMessage(f"Process {totalRecords:,} routes")  

        #========== Process Routes to Horizontal Routes ======================
        
        arcpy.AddMessage("="*100)
        with arcpy.da.SearchCursor(input_routeLayer, fields) as sCursor:
            for index, row in enumerate(sCursor):
                index += 1
                rid = row[fields.index(input_route_rid)]
                arcpy.SetProgressorLabel(f"Processing {index:,} out of {totalRecords} Routes")
                arcpy.AddMessage(f"Starting Horizontal Process for Route {rid}")
                
                polyline = row[0]
                firstPoint = 0 if not bool(input_bool_measS) else float(str(polyline.firstPoint).split(' ')[-1])
                firstMeas = row[fields.index(input_froMeas)] if not bool(input_bool_measS) else firstPoint
                first_point = arcpy.Point(0,
                                          0,
                                          0,
                                          firstMeas)
                
                lastPoint = polyline.length if not bool(input_bool_measS) else float(str(polyline.lastPoint).split(' ')[-1])
                lastMeas = row[fields.index(input_toMeas)] if not bool(input_bool_measS) else lastPoint
                last_point = arcpy.Point(polyline.length, 
                                         0,
                                         0,
                                         lastMeas)
                
                array = arcpy.Array([first_point, last_point])
                horizontal_line = arcpy.Polyline(array)
                with arcpy.da.InsertCursor(routeLayerCopy, fields) as iCursor:
                    iField = [r for r in row[1:]]
                    iField.insert(0, horizontal_line)
                    iCursor.insertRow(iField)
                arcpy.SetProgressorPosition()
        arcpy.ResetProgressor()
        arcpy.AddMessage("="*100)
        #========== Process Routes to Horizontal Routes ======================

        #========== Store Horizontal Routes ======================
        arcpy.SetProgressor('default', "Storing Routes...")  
        # Create a GDB to store result
        outputName_ = outputName if not outputName.endswith('.gdb') else outputName.replace('.gdb','')
        dirName = os.path.dirname(arcpy.env.workspace)
        arcpy.management.CreateFileGDB(dirName, outputName_)
        fcName = _extract_alphanumeric(os.path.basename(input_routeLayer))
        
        try:
            arcpy.conversion.ExportFeatures(routeLayerCopy,
                                        f"{dirName}/{outputName_}.gdb/{fcName}",
                                        sort_field=[input_froMeas])
        except:
            arcpy.conversion.ExportFeatures(routeLayerCopy,
                                        f"{dirName}/{outputName_}.gdb/{fcName}")
        arcpy.ResetProgressor()
        arcpy.AddMessage(f'GDB Stored at {os.path.join(dirName, outputName_)}.gdb')
        #========== Store Horizontal Routes ======================

        # Delete copies
        for fc in deleteList:
            arcpy.management.Delete(fc)
        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return

class GenerateHorizontalRouteEvent:
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "2) Generate Horizontal Route Event"
        self.description = "This GP tool generates horizontal events"

    def getParameterInfo(self):
        """Define the tool parameters."""
        params0 = arcpy.Parameter()
        params0.name = 'input_sld_route'
        params0.displayName = 'Input Route SLD Feature'
        params0.parameterType = 'Required'
        params0.direction = 'Input'
        params0.datatype = 'GPFeatureLayer'
        params0.filter.list = ['POLYLINE']
        params0.displayOrder = 1

        params1 = arcpy.Parameter()
        params1.name = 'input_sld_rid_field'
        params1.displayName = "Route Identifier Field"
        params1.parameterType = 'Required'
        params1.direction = 'Input'
        params1.datatype = 'Field'
        params1.parameterDependencies = [params0.name]
        params0.displayOrder =2

        params2 = arcpy.Parameter()
        params2.name = 'input_event_type'
        params2.displayName = "Event Type"
        params2.parameterType = 'Required'
        params2.direction = 'Input'
        params2.datatype = 'GPString'
        params2.filter.list = ["POINT", 'LINE']
        params2.displayOrder =3

        params3 = arcpy.Parameter()
        params3.name = 'input_event_lyr'
        params3.displayName = "Input Event Layer"
        params3.parameterType = 'Required'
        params3.direction = 'Input'
        params3.datatype = 'GPFeatureLayer'
        params3.displayOrder = 4

        params4 = arcpy.Parameter()
        params4.name = 'input_event_rid_field'
        params4.displayName = "Route Identified Field"
        params4.parameterType = 'Required'
        params4.direction = 'Input'
        params4.datatype = 'Field'
        params4.parameterDependencies = [params3.name]
        params4.displayOrder = 5

        params5 = arcpy.Parameter()
        params5.name = 'input_event_pMeas_field'
        params5.displayName = "Point Event Measure Field"
        params5.parameterType = 'Optional'
        params5.direction = 'Input'
        params5.datatype = 'Field'
        params5.parameterDependencies = [params3.name]
        params5.displayOrder = 6
        params5.enabled = False
        
        params6 = arcpy.Parameter()
        params6.name = 'input_event_fMeas_field'
        params6.displayName = "Line Event From-Measure Field"
        params6.parameterType = 'Optional'
        params6.direction = 'Input'
        params6.datatype = 'Field'
        params6.parameterDependencies = [params3.name]
        params6.displayOrder = 7
        params6.enabled = False

        params7 = arcpy.Parameter()
        params7.name = 'input_event_tMeas_field'
        params7.displayName = "Line Event To-Measure Field"
        params7.parameterType = 'Optional'
        params7.direction = 'Input'
        params7.datatype = 'Field'
        params7.parameterDependencies = [params3.name]
        params7.displayOrder = 7
        params7.enabled = False

        params8 =arcpy.Parameter()
        params8.name = 'input_event_locError'
        params8.displayName = "Generate a field for locating errors"
        params8.parameterType = 'Optional'
        params8.direction = 'Input'
        params8.datatype = 'Boolean'
        params8.value = True
        params8.displayOrder = 8
        

        return [params0,
                params1,
                params2,
                params3,
                params4,
                params5,
                params6,
                params7,
                params8]

    def isLicensed(self):
        """Set whether the tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""

        # Update the Event Layer from user Input
        if parameters[2].altered:
            if parameters[2].valueAsText =='POINT':
                parameters[3].filter.list = ["POINT"]
                parameters[5].enabled = True
                parameters[6].enabled = False
                parameters[7].enabled = False
            else:
                parameters[3].filter.list = ["POLYLINE"]
                parameters[6].enabled = True
                parameters[7].enabled = True

                parameters[5].enabled = False
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter. This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        # Set Variables
        inputRT_SLD = parameters[0].valueAsText
        inputRT_RID = parameters[1].valueAsText
        inputEvent_Type = parameters[2].valueAsText
        inputEvent_Lyr = parameters[3].valueAsText
        inputEvent_RID = parameters[4].valueAsText
        inputEvent_P_Meas = parameters[5].valueAsText
        inputEvent_L_FMeas = parameters[6].valueAsText
        inputEvent_L_TMeas =parameters[7].valueAsText
        inputEvent_LOCE = parameters[8].value
        deleteList = []
        eventRecCnt = int(arcpy.management.GetCount(inputEvent_Lyr)[0])

        arcpy.AddMessage(f"Starting Process on {os.path.basename(inputEvent_Lyr)} Event Layer")

        #========== Process Event Exoport 2 Table ======================
        # Create a copy of the Input Rotue Layer
        eventLyrName = os.path.basename(inputEvent_Lyr).replace('\\','').replace(' ','')
        eventLyrCopy = arcpy.CreateScratchName(eventLyrName, 
                                                 'FeatureDataset ',
                                                 arcpy.env.workspace)
        deleteList.append(eventLyrCopy)        
        sortField = inputEvent_P_Meas if inputEvent_Type =='POINT' else inputEvent_L_FMeas
        arcpy.SetProgressor('default', "Obtaining Event Table...")  
        arcpy.conversion.ExportTable(inputEvent_Lyr, eventLyrCopy, sort_field=sortField)
        arcpy.ResetProgressor()
        arcpy.AddMessage(f"Event tabled obtained\nProceeding to create Event SLD")
        #========== Process Event Exoport 2 Table ======================

        #========== Process Event SLD             ======================
        arcpy.SetProgressor('default', f"Converting {os.path.basename(inputEvent_Lyr)} Event to a SLD...")  
        arcpy.AddMessage(f"Conversion for {os.path.basename(inputEvent_Lyr)} to SLD starting")
        eventView = f"{eventLyrName}View"
        deleteList.append(eventView)
        if inputEvent_Type == "POINT":
            arcpy.lr.MakeRouteEventLayer(
                in_routes= inputRT_SLD,
                route_id_field=inputRT_RID,
                in_table=eventLyrCopy,
                in_event_properties= f"{inputEvent_RID}; {inputEvent_Type}; {inputEvent_P_Meas}",
                out_layer=eventView,
                offset_field=None,
                add_error_field="ERROR_FIELD" if bool(inputEvent_LOCE) else "NO_ERROR_FIELD")
        else:
            arcpy.lr.MakeRouteEventLayer(
                in_routes= inputRT_SLD,
                route_id_field=inputRT_RID,
                in_table=eventLyrCopy,
                in_event_properties= f"{inputEvent_RID}; {inputEvent_Type}; {inputEvent_L_FMeas}; {inputEvent_L_TMeas}",
                out_layer=eventView,
                offset_field=None,
                add_error_field="ERROR_FIELD" if bool(inputEvent_LOCE) else "NO_ERROR_FIELD",
                add_angle_field="NO_ANGLE_FIELD")
        arcpy.ResetProgressor()
        arcpy.AddMessage(f"Conversion completed...\nSaving results")  
        #========== Save Event SLD            ======================
        arcpy.SetProgressor('default', f"Saving Results")  
        gdbDir = _getCatalogPath(inputRT_SLD)['dir']
        outputEventSld = os.path.join(gdbDir, eventLyrName)
        arcpy.conversion.ExportFeatures(eventView,outputEventSld)
        arcpy.ResetProgressor()
        arcpy.AddMessage(f"Results saved at {gdbDir}")
        #========== Save Event SLD            ======================

        for fc in deleteList:
            arcpy.management.Delete(fc)
        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return
