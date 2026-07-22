import pandas as pd

EXCEL_FILE = "data/Vehicle_Health_System_Data.xlsx"


def load_data():

    thresholds = pd.read_excel(
        EXCEL_FILE,
        sheet_name="Standard_Thresholds"
    )

    sensor_data = pd.read_excel(
        EXCEL_FILE,
        sheet_name="Vehicle_Dummy_Data"
    )

    owner_data = pd.read_excel(
        EXCEL_FILE,
        sheet_name="Vehicle_Master"
    )

    vehicle_data = pd.read_excel(
        EXCEL_FILE,
        sheet_name="Vehicle_Details"
    )

    service_data = pd.read_excel(
        EXCEL_FILE,
        sheet_name="Service_History"
    )

    return (
        thresholds,
        sensor_data,
        owner_data,
        vehicle_data,
        service_data
    )
