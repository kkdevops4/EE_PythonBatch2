import numpy as np

class DataAnalyzer:
    def __init__(self, data):
        self.data = data

    def dataset_summary(self):
        print("\n" + "-" * 60)
        print("DATASET SUMMARY")
        print("-" * 60)
        print("Total Records :", len(self.data))
        print("Total Drivers :", self.data["Driver_ID"].nunique())
        print("Total Columns :", len(self.data.columns))
        print("Missing Values :", self.data.isnull().sum().sum())

    def overall_statistics(self):
        print("\n" + "-" * 60)
        print("OVERALL SENSOR STATISTICS")
        print("-" * 60)
        print("Average Eye Closure :", round(np.mean(self.data["Eye_Closure_%"]), 2))
        print("Average Blink Rate :", round(np.mean(self.data["Blink_Rate"]), 2))
        print("Average Head Pitch :", round(np.mean(self.data["Head_Pitch_Angle"]), 2))
        print("Average Yawning :", round(np.mean(self.data["Yawning_Count"]), 2))
        print("Average Distance :", round(np.mean(self.data["Travel_Distance_km"]), 2))

    def calculated_score_analysis(self, calculated_data):
        print("\n" + "-" * 60)
        print("CALCULATED ATTENTIVENESS ANALYSIS")
        print("-" * 60)
        print("Average Calculated Score :", round(calculated_data["Attention_Score"].mean(), 2))
        print("Calculated Status Counts:")
        print(calculated_data["Attention_Status"].value_counts())

    def driver_summary(self, calculated_data):
        summary = calculated_data.groupby(["Driver_ID", "Driver_Name"]).agg(
            Average_Eye_Closure=("Eye_Closure_%", "mean"),
            Average_Blink_Rate=("Blink_Rate", "mean"),
            Average_Head_Pitch=("Head_Pitch_Angle", "mean"),
            Total_Yawns=("Yawning_Count", "sum"),
            Average_Attention_Score=("Attention_Score", "mean")).reset_index().round(2)

        print("\n" + "-" * 60)
        print("CALCULATED DRIVER SUMMARY")
        print("-" * 60)
        print(summary.to_string(index=False))
        return summary

    def shift_summary(self, calculated_data):
        summary = calculated_data.groupby(["Driver_Name", "Shift"]).agg(
            Eye_Closure=("Eye_Closure_%", "mean"),
            Blink_Rate=("Blink_Rate", "mean"),
            Head_Pitch=("Head_Pitch_Angle", "mean"),
            Yawning=("Yawning_Count", "sum"),
            Attention_Score=("Attention_Score", "mean")).reset_index().round(2)

        print("\n" + "-" * 60)
        print("CALCULATED SHIFT-WISE SUMMARY")
        print("-" * 60)
        print(summary.to_string(index=False))
        return summary