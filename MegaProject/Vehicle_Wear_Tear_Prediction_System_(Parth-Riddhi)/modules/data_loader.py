

import pandas as pan 

def load_data():
    threshold_data = pan.read_excel("dataset/Standard_Vehicle_Data.xlsx" , sheet_name="Standard_Thresholds")

    dummy_data = pan.read_excel("dataset/Standard_Vehicle_Data.xlsx" , sheet_name="Vehicle_Dummy_Data")

    return threshold_data, dummy_data