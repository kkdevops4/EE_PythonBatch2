from data_loader import load_data
from comparator import analyze_vehicle
from health_score import calculate_health_score
from recommendation import generate_recommendations
from visualization import (
    generate_pie_chart
)
from pdf_generator import generate_pdf

def main():

    print("=" * 60)
    print("VEHICLE WEAR & TEAR PREDICTION SYSTEM")
    print("=" * 60)

    # Load all sheets
    (
        thresholds_df,
        sensor_df,
        owner_df,
        vehicle_df,
        service_df
    ) = load_data()

    # User Input
    vehicle_number = input(
        "\nEnter Vehicle Number : "
    ).strip()

    # Search Vehicle
    vehicle_match = vehicle_df[
        vehicle_df["Vehicle_Number"] == vehicle_number
    ]

    if vehicle_match.empty:
        print("\nVehicle not found!")
        return

    vehicle_row = vehicle_match.iloc[0]

    vehicle_id = vehicle_row["Vehicle_ID"]

    print(f"\nVehicle Found : {vehicle_id}")

    # Fetch Owner Details
    owner_row = owner_df[
        owner_df["Vehicle_ID"] == vehicle_id
    ]

    if owner_row.empty:
        print("Owner details not found.")
        return

    owner_row = owner_row.iloc[0]

    # Fetch Sensor Data
    sensor_row = sensor_df[
        sensor_df["Vehicle_ID"] == vehicle_id
    ]

    if sensor_row.empty:
        print("Sensor data not found.")
        return

    sensor_row = sensor_row.iloc[0]

    # Fetch Service Data
    service_row = service_df[
        service_df["Vehicle_ID"] == vehicle_id
    ]

    if not service_row.empty:
        service_row = service_row.iloc[0]
    else:
        service_row = None

    print("\nAnalyzing vehicle sensors...")

    # Analyze Sensors
    results = analyze_vehicle(sensor_row)

    # Calculate Health Score
    health_score = calculate_health_score(results)

    # Generate Recommendations
    recommendations = generate_recommendations(results)

    print("\nGenerating Charts...")

    # Generate Graphs
    generate_pie_chart(results)

    print("Generating PDF Report...")

    # Generate PDF
    generate_pdf(
        vehicle_id=vehicle_id,
        owner_info=owner_row,
        vehicle_info=vehicle_row,
        service_info=service_row,
        score=health_score,
        recommendations=recommendations,
        results=results,
        thresholds_df=thresholds_df
    )

    # Console Output
    print("\n" + "=" * 60)
    print("REPORT SUMMARY")
    print("=" * 60)

    print(f"\nVehicle ID       : {vehicle_id}")
    print(
        f"Owner Name       : "
        f"{owner_row['Owner_Name']}"
    )
    print(
        f"Vehicle Number   : "
        f"{vehicle_row['Vehicle_Number']}"
    )

    print(
        f"\nOverall Health Score : "
        f"{health_score}%"
    )

    green_count = sum(
        1 for sensor in results.values()
        if sensor["status"] == "GREEN"
    )

    yellow_count = sum(
        1 for sensor in results.values()
        if sensor["status"] == "YELLOW"
    )

    red_count = sum(
        1 for sensor in results.values()
        if sensor["status"] == "RED"
    )

    print(f"\nGREEN  Sensors : {green_count}")
    print(f"YELLOW Sensors : {yellow_count}")
    print(f"RED    Sensors : {red_count}")

    print("\nRecommendations:")

    for rec in recommendations:
        print(f"• {rec}")

    print(
        f"\nPDF Report Generated Successfully"
        f"\nLocation : reports/{vehicle_id}.pdf"
    )

    print("\nDone!")
    
if __name__ == "__main__":
    main()