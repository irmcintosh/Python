# Given dataset
dataset = [
    {'OID': 1, 'RouteID': 'Ackerly Farm Rd|New Albany', 'Beg_Log': 0, 'End_Log': 1},
    {'OID': 2, 'RouteID': 'Ackerly Farm Rd|New Albany', 'Beg_Log': 0, 'End_Log': 2},
    {'OID': 3, 'RouteID': 'Ackerly Farm Rd|New Albany', 'Beg_Log': 0, 'End_Log': 3}
]

# Fixing the dataset
for i in range(1, len(dataset)):
    dataset[i]['Beg_Log'] = dataset[i - 1]['End_Log']
dataset[-1]['End_Log'] = len(dataset)

# Updated dataset
for data in dataset:
    print(data)
