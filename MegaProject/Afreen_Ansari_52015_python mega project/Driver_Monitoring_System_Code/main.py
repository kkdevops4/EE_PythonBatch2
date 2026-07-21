import os
import shutil

from word_to_pdf import convert_word_to_pdf
from modules.loader import DataLoader
from modules.evaluator import DriverEvaluator
from modules.report import WordReport

def create_folders():
    folders = ["data","reports","backup"]
    for folder in folders:
        os.makedirs(folder,exist_ok=True)

def backup_dataset(file_path):
    if not os.path.exists(file_path):
        return
    try:
        shutil.copy(file_path,"backup/DMS_Dataset_Backup.xlsx")
    except PermissionError:
        pass

def show_driver_results(ranking):
    print("\n" + "=" * 80)
    print("DRIVER OVERALL SCORE COMPARISON")
    print("=" * 80)
    results = ranking[[
            "Driver_Name",
            "Driver_ID",
            "Overall_Score",
            "Overall_Status"]].copy()

    results = results.rename(columns={
            "Driver_Name":
                "Driver Name",
            "Driver_ID":
                "Driver ID",
            "Overall_Score":
                "Overall Score",
            "Overall_Status":
                "Overall Status"})
    print(results.to_string(index=False))
    best_driver = ranking.iloc[0]
    print("\n" + "-" * 80)
    print("BEST DRIVER:",best_driver["Driver_Name"])
    print("BEST DRIVER ID:",best_driver["Driver_ID"])
    print("BEST SCORE:",f"{best_driver['Overall_Score']:.2f}/100")
    print("BEST STATUS:",best_driver["Overall_Status"])
    print("-" * 80)

def main():
    create_folders()
    dataset_path = ("data/DMS_Final_Workbook_Final.xlsx")
    backup_dataset(dataset_path)
    loader = DataLoader(dataset_path)
    data = loader.load_data()
    if data is None:
        print("Dataset could not be loaded.")
        return
    evaluator = DriverEvaluator(data)
    driver_report = (evaluator.calculate_scores())
    calculated_data = evaluator.data
    ranking = evaluator.create_ranking(driver_report)
    show_driver_results(ranking)
    report = WordReport(calculated_data,driver_report,ranking)
    word_report = report.generate_report()
   
    pdf_report = convert_word_to_pdf(word_report)
    print("\n" + "=" * 80)
    print("WORD REPORT LOCATION:")
    print(word_report)
    if pdf_report is not None:
        print("\nPDF REPORT LOCATION:")
        print(os.path.relpath(pdf_report))
    print("=" * 80)

if __name__ == "__main__":
    main()