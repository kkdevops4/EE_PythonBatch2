import pandas as pan


def generate_txt_report(vehicle_id,status,alert,recommendation):

    with open(f"reports/{vehicle_id}.txt","w") as fd:

        fd.write("==================================================\n")
        fd.write("        VEHICLE WEAR & TEAR REPORT\n")
        fd.write("==================================================\n\n")

        fd.write(f"Vehicle ID       : {vehicle_id}\n\n")
        fd.write(f"Status           : {status}\n\n")
        fd.write(f"Alert            : {alert}\n\n")
        fd.write(f"Recommendation   : {recommendation}\n\n")

        fd.write("==================================================\n")


def generate_excel_report(all_vehicle_data):

    data_frame = pan.DataFrame(all_vehicle_data)

    data_frame.to_excel("reports/vehicle_report.xlsx",index=False)

    print("\nExcel Report Generated Successfully!")