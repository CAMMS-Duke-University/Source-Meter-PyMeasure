from pymeasure.instruments import list_resources

connected_instument_names = []
for list_item in list_resources():
    connected_instument_names.append(list_item)

connected_instument_names.pop(0)

print("-------")

print(connected_instument_names)
