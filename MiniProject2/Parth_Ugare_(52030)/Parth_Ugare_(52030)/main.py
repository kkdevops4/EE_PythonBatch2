# modules ;->
from modules import generator,storage,analyze,report

if __name__ == "__main__":
    print("Tyre Wear Analyzer")


    '''
    flow :-
    generator -> storage -> analyzer -> report 
    '''

    generator_obj = generator.TyreDataGenerator()
    data_readings = generator_obj.generate_reading()

    storage_obj = storage.DataStorage()
    storage_obj.save_data(data_readings)
    json_data = storage_obj.load_data()

    analyzer_obj = analyze.TyreAnalyzer()
    tyre_data = analyzer_obj.analyze()
    new_sorted_data = analyzer_obj.sort_data(tyre_data)
    tyre_severity_data = analyzer_obj.check_severity(new_sorted_data)

    report_txt = report.show_report(tyre_severity_data)
    report.print_report(report_txt)
    report.save_report(report_txt)

