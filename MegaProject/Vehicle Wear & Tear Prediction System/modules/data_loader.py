

import pandas as pan 

file_path = "dataset/Standard_Vehicle_Data.xlsx"


def load_data():

    threshold_data = pan.read_excel(file_path , sheet_name="Standard_Thresholds")

    dummy_data = pan.read_excel(file_path , sheet_name="Vehicle_Dummy_Data")

    owner_data = pan.read_excel(file_path, sheet_name="Vehicle_Master")

    vehicle_data = pan.read_excel(file_path, sheet_name="Vehicle_Details")

    service_data = pan.read_excel(file_path, sheet_name="Service_History")

    return threshold_data, dummy_data, owner_data, vehicle_data, service_data