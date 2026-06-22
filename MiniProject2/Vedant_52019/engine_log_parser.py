import os
import json

# Empty list to store all warnings and errors
all_logs = []

# Folder containing log files
logs_folder = "logs"

# Search all folders and files
for root, dirs, files in os.walk(logs_folder):

    # Check every file
    for file in files:

        # Process only .log files
        if file.endswith(".log"):

            file_path = os.path.join(root, file)

            print("Reading:", file_path)

            # Open file using context manager
            with open(file_path, "r") as log_file:

                lines = log_file.readlines()

                # Read line by line
                for i in range(len(lines)):

                    current_line = lines[i].strip()

                    # Check for WARNING or ERROR
                    if "WARNING" in current_line or "ERROR" in current_line:

                        # Extract date
                        date = current_line.split("]")[0]
                        date = date.replace("[", "")

                        # Remove date part
                        remaining_text = current_line.split("]")[1].strip()

                        # Split level and message
                        parts = remaining_text.split(" ", 1)

                        level = parts[0]

                        if len(parts) > 1:
                            message = parts[1]
                        else:
                            message = ""

                        # Default source
                        source = "Unknown"

                        # Check next line for source
                        if i + 1 < len(lines):

                            next_line = lines[i + 1].strip()

                            if next_line.startswith("Source:"):

                                source = next_line.replace("Source:", "").strip()

                        # Create dictionary
                        log_data = {
                            "date": date,
                            "level": level,
                            "message": message,
                            "source": source
                        }

                        # Add to list
                        all_logs.append(log_data)

# Create JSON report
with open("engine_report.json", "w") as json_file:

    json.dump(all_logs, json_file, indent=4)

print("\nJSON report generated successfully!")
print("Total warnings/errors found:", len(all_logs))