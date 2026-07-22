import numpy as np
import pandas as pd

class DriverEvaluator:
    EYE_WEIGHT = 0.35
    BLINK_WEIGHT = 0.25
    HEAD_WEIGHT = 0.25
    YAWN_WEIGHT = 0.15

    def __init__(self, data):
        self.data = data.copy()

    def eye_score(self, value):
        if value <= 5:
            return 100
        if value <= 10:
            return 85
        if value <= 15:
            return 65
        if value <= 20:
            return 40
        return 15

    def blink_score(self, value):
        if 12 <= value <= 20:
            return 100
        if 10 <= value < 12:
            return 75
        if 8 <= value < 10:
            return 50
        if value < 8:
            return 20
        if value <= 25:
            return 80
        return 50

    def head_score(self, value):
        value = abs(value)
        if value <= 5:
            return 100
        if value <= 10:
            return 80
        if value <= 15:
            return 55
        return 20

    def yawn_score(self, value):
        if value <= 0:
            return 100
        if value == 1:
            return 65
        return 20

    def status(self, score):
        if score >= 85:
            return "Attentive"
        if score >= 70:
            return "Moderately Attentive"
        return "Inattentive"

    def recommendation(self, status):
        if status == "Attentive":
            return "Attention is satisfactory. Continue normal driving."
        if status == "Moderately Attentive":
            return "Minor fatigue indicators detected. Take a short break."
        return "Serious fatigue indicators detected. Stop and take sufficient rest."

    def calculate_row_scores(self):
        self.data["Eye_Score"] = self.data["Eye_Closure_%"].apply(self.eye_score)
        self.data["Blink_Score"] = self.data["Blink_Rate"].apply(self.blink_score)
        self.data["Head_Score"] = self.data["Head_Pitch_Angle"].apply(self.head_score)
        self.data["Yawning_Score"] = self.data["Yawning_Count"].apply(self.yawn_score)
        self.data["Attention_Score"] = (self.data["Eye_Score"] * self.EYE_WEIGHT
            + self.data["Blink_Score"] * self.BLINK_WEIGHT
            + self.data["Head_Score"] * self.HEAD_WEIGHT
            + self.data["Yawning_Score"] * self.YAWN_WEIGHT).round(2)
        self.data["Attention_Status"] = self.data["Attention_Score"].apply(self.status)
        return self.data

    def calculate_scores(self):
        self.calculate_row_scores()

        report = self.data.groupby(
            ["Driver_ID", "Driver_Name", "Shift"]).agg(
            Duration=("Time_Minutes", "count"),
            Distance=("Travel_Distance_km", "max"),
            Eye_Closure=("Eye_Closure_%", "mean"),
            Blink_Rate=("Blink_Rate", "mean"),
            Head_Pitch=("Head_Pitch_Angle", "mean"),
            Yawning=("Yawning_Count", "sum"),
            Eye_Score=("Eye_Score", "mean"),
            Blink_Score=("Blink_Score", "mean"),
            Head_Score=("Head_Score", "mean"),
            Yawning_Score=("Yawning_Score", "mean"),
            Attention_Score=("Attention_Score", "mean")).reset_index()

        numeric = ["Distance", "Eye_Closure", "Blink_Rate", "Head_Pitch",
            "Eye_Score", "Blink_Score", "Head_Score", "Yawning_Score",
            "Attention_Score"]
        report[numeric] = report[numeric].round(2)
        report["Status"] = report["Attention_Score"].apply(self.status)
        report["Recommendation"] = report["Status"].apply(self.recommendation)

        shift_type = pd.CategoricalDtype(["Morning", "Afternoon", "Night"],ordered=True)
        report["Shift"] = report["Shift"].astype(shift_type)
        return report.sort_values(["Driver_Name", "Shift"]).reset_index(drop=True)

    def create_ranking(self, driver_report):
        ranking = driver_report.groupby(["Driver_ID", "Driver_Name"]).agg(
            Overall_Score=("Attention_Score", "mean"),
            Average_Eye_Score=("Eye_Score", "mean"),
            Average_Blink_Score=("Blink_Score", "mean"),
            Average_Head_Score=("Head_Score", "mean"),
            Average_Yawning_Score=("Yawning_Score", "mean"),
            Total_Distance=("Distance", "max"),
            Average_Eye_Closure=("Eye_Closure", "mean"),
            Average_Blink_Rate=("Blink_Rate", "mean"),
            Average_Head_Pitch=("Head_Pitch", "mean"),
            Total_Yawns=("Yawning", "sum")).reset_index()

        numeric = ranking.select_dtypes(include=[np.number]).columns
        ranking[numeric] = ranking[numeric].round(2)
        ranking["Overall_Status"] = ranking["Overall_Score"].apply(self.status)
        ranking = ranking.sort_values("Overall_Score", ascending=False).reset_index(drop=True)
        ranking.insert(0, "Rank", ranking.index + 1)
        return ranking
