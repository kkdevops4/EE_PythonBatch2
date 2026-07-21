from modules.excel_reader import ExcelReader
class ACCValidator:
    MIN_ACTIVATION_SPEED_KMH = 25       # ACC won't engage below this
    EMERGENCY_DISTANCE_M = 10           # <= this + closing gap -> emergency brake
    CUT_IN_DISTANCE_M = 15              # <= this -> controlled deceleration
    SAFE_DISTANCE_M = 30                # <= this with a small speed gap -> "safe"
    LARGE_SPEED_GAP_KMH = 10            # gap above this -> actively reduce speed
    STOP_AND_GO_SPEED_KMH = 30          # own speed at/below this + stopped lead -> stop/go
    SET_SPEED_STEP_KMH = 5              # +/- button increment

    MISSING_RESULT = "Missing Value Error"
    INVALID_RESULT = "Invalid Value Error"

    ACTION_REQUIRED_FIELDS = {
        "acc_on": ["Vehicle_Speed"],
        "set_speed": ["Set_Speed"],
        "increase_setspeed": ["Set_Speed"],
        "decrease_setspeed": ["Set_Speed"],
        "resume": ["Set_Speed"],
        "brake_pedal": [],
        "acc_cancel": [],
        "radar_failure": [],
        "camera_failure": [],
        "accelerator": [],
        "ignition_off": [],
    }

    @staticmethod
    def validate(row):
        problem = ACCValidator._field_problem(row, "Ignition_Status")
        if problem:
            return problem
        problem = ACCValidator._field_problem(row, "User_Action")
        if problem:
            return problem

        ignition = str(row["Ignition_Status"]).strip().upper()
        action = str(row["User_Action"]).strip().lower()

        if ignition == "OFF":
            return "ACC Disabled", "Ignition Off - ACC Disengaged"

        # Action-specific required fields
        if action == "maintain":
            problem = ACCValidator._maintain_field_problem(row)
        else:
            problem = None
            for field in ACCValidator.ACTION_REQUIRED_FIELDS.get(action, []):
                problem = ACCValidator._field_problem(row, field)
                if problem:
                    break
        if problem:
            return problem

        vehicle_speed = row["Vehicle_Speed"]
        set_speed = row["Set_Speed"]
        lead_detected = str(row["Lead_Vehicle_Detected"]).strip().upper()
        lead_speed = row["Lead_Vehicle_Speed"]
        distance = row["Following_Distance"]

        if action == "acc_on":
            if vehicle_speed >= ACCValidator.MIN_ACTIVATION_SPEED_KMH:
                return (
                    "ACC Activated",
                    f"Vehicle Speed {ACCValidator._fmt(vehicle_speed)} km/h "
                    f"At Or Above Minimum Threshold ({ACCValidator.MIN_ACTIVATION_SPEED_KMH} km/h)",
                )
            return (
                f"Min Speed To Activate ACC Is {ACCValidator.MIN_ACTIVATION_SPEED_KMH} km/hr",
                f"Vehicle Speed {ACCValidator._fmt(vehicle_speed)} km/h Below Minimum Threshold",
            )

        if action == "set_speed":
            return f"Set Speed = {ACCValidator._fmt(set_speed)}", "Set Speed Stored"

        if action == "increase_setspeed":
            new_speed = set_speed + ACCValidator.SET_SPEED_STEP_KMH
            return f"Set Speed = {ACCValidator._fmt(new_speed)}", "Set Speed Incremented"

        if action == "decrease_setspeed":
            new_speed = set_speed - ACCValidator.SET_SPEED_STEP_KMH
            return f"Set Speed = {ACCValidator._fmt(new_speed)}", "Set Speed Decremented"

        if action == "brake_pedal":
            return "ACC Deactivated", "Brake Pedal Pressed"

        if action == "acc_cancel":
            return "ACC Deactivated", "Cancel Button Pressed"

        if action == "resume":
            return (
                f"Speed Restored to {ACCValidator._fmt(set_speed)} km/h",
                "Resume Button Pressed",
            )

        if action == "radar_failure":
            return "ACC Disabled, Warning Displayed", "Radar Signal Lost"

        if action == "camera_failure":
            return "ACC Disabled, Warning Displayed", "Camera Signal Lost"

        if action == "accelerator":
            return "Manual Override Allowed", "Driver Accelerator Override"

        if action == "ignition_off":
            return "ACC Disabled", "Ignition Turned Off"

        if action == "maintain":
            return ACCValidator._evaluate_driving_scenario(
                vehicle_speed, set_speed, lead_detected, lead_speed, distance
            )
        return "Invalid Action", "Unknown Action"

    @staticmethod
    def _evaluate_driving_scenario(vehicle_speed, set_speed, lead_detected, lead_speed, distance):
        remarks = []

        # No lead vehicle: ACC simply holds / returns to the set speed
        if lead_detected != "YES":
            if vehicle_speed == set_speed:
                remarks.append("No Lead Vehicle - Holding Set Speed")
                return f"Vehicle Maintains {ACCValidator._fmt(set_speed)} km/h", ", ".join(remarks)
            elif vehicle_speed < set_speed:
                remarks.append("Lane Clear - Accelerating to Set Speed")
                return f"Speed Increased to {ACCValidator._fmt(set_speed)} km/h", ", ".join(remarks)
            else:
                remarks.append("Lane Clear - Decelerating to Set Speed")
                return f"Speed Decreased to {ACCValidator._fmt(set_speed)} km/h", ", ".join(remarks)

        # A lead vehicle is present - evaluate distance / closing speed
        speed_gap = vehicle_speed - lead_speed

        # Stopped/near-stopped lead vehicle in slow traffic
        if lead_speed == 0 and vehicle_speed <= ACCValidator.STOP_AND_GO_SPEED_KMH:
            remarks.append("Stop-and-Go Traffic Detected")
            return "Vehicle Stops and Resumes", ", ".join(remarks)

        # Very close + closing -> emergency braking
        if distance <= ACCValidator.EMERGENCY_DISTANCE_M:
            remarks.append("Critical Distance - Sudden Braking of Lead Vehicle")
            return "Emergency Deceleration", ", ".join(remarks)

        # Close, likely a cut-in -> controlled deceleration
        if distance <= ACCValidator.CUT_IN_DISTANCE_M:
            remarks.append("Vehicle Cut-In Detected")
            return "Controlled Deceleration", ", ".join(remarks)

        # Meaningfully faster than the lead vehicle -> actively slow to match
        if speed_gap > ACCValidator.LARGE_SPEED_GAP_KMH:
            remarks.append("Lead Vehicle Slower - Adjusting Speed")
            return f"Speed Reduced to {ACCValidator._fmt(lead_speed)} km/h", ", ".join(remarks)

        # Within a comfortable following distance and speeds roughly matched
        if distance <= ACCValidator.SAFE_DISTANCE_M:
            remarks.append("Following Distance Within Safe Range")
            return "Safe Distance Maintained", ", ".join(remarks)

        remarks.append("Lead Vehicle Within Radar/Camera Range")
        return "Lead Vehicle Detected", ", ".join(remarks)

    @staticmethod
    def _maintain_field_problem(row):
        for field in ("Vehicle_Speed", "Set_Speed"):
            problem = ACCValidator._field_problem(row, field)
            if problem:
                return problem

        problem = ACCValidator._field_problem(row, "Lead_Vehicle_Detected")
        if problem:
            return problem

        if str(row["Lead_Vehicle_Detected"]).strip().upper() == "YES":
            for field in ("Lead_Vehicle_Speed", "Following_Distance"):
                problem = ACCValidator._field_problem(row, field)
                if problem:
                    return problem
        return None

    @staticmethod
    def _field_problem(row, field):

        tc_id = row.get("TC_ID", "?")
        excel_row = row.get("Excel_Row", "?")
        label = ExcelReader.DISPLAY_LABELS.get(field, field.replace("_", " "))

        if row.get(f"_missing__{field}", False):
            return (
                ACCValidator.MISSING_RESULT,
                f"Missing Value Error: Column '{label}' is empty "
                f"(Test Case {tc_id}, Row {excel_row}).",
            )

        if row.get(f"_invalid__{field}", False):
            reason = row.get(f"_invalid_reason__{field}", "")
            return (
                ACCValidator.INVALID_RESULT,
                f"Invalid Value Error: Column '{label}' {reason} "
                f"(Test Case {tc_id}, Row {excel_row}).",
            )

        return None

    @staticmethod
    def explain_mismatch(actual_result, expected_result, simulated_result, simulated_remarks):
        actual_n = str(actual_result).strip().lower()
        expected_n = str(expected_result).strip().lower()
        simulated_n = str(simulated_result).strip().lower()

        if simulated_result in (ACCValidator.MISSING_RESULT, ACCValidator.INVALID_RESULT):
            return (
                f"Recorded Actual Result '{actual_result}' does not match the Expected "
                f"Result '{expected_result}', and the input parameters for this row also "
                f"failed validation ({simulated_remarks})."
            )

        if actual_n == simulated_n and simulated_n != expected_n:
            return (
                f"The recorded Actual Result matches what the ACC logic predicts for these "
                f"inputs ('{simulated_result}' - {simulated_remarks}), but the sheet's "
                f"Expected Result reads '{expected_result}'. The documented expectation "
                f"looks out of date for this scenario rather than the system misbehaving."
            )

        if actual_n != simulated_n:
            return (
                f"For these input parameters the ACC logic predicts '{simulated_result}' "
                f"({simulated_remarks}), but the recorded Actual Result is "
                f"'{actual_result}'. This looks like a genuine functional deviation rather "
                f"than a documentation issue."
            )

        return (
            f"Actual Result '{actual_result}' does not textually match the documented "
            f"Expected Result '{expected_result}', although both agree with the ACC logic "
            f"prediction for these inputs - check for wording/formatting differences."
        )

    @staticmethod
    def _fmt(value):
        """Formats whole-number speeds without a trailing '.0'."""
        return int(value) if float(value).is_integer() else value
