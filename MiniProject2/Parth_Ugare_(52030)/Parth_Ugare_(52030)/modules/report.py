
# import modules.analyze as analyze


def show_report(result):
    action_take = {
        "High": {
            "action":"Replace tyre",
            "priority":"URGENT"
        },
        "Medium":{
            "action":"Inspect tyre soon",
            "priority":"WARNING"
        },
        "Good":{
            "action":"Normal Condition",
            "priority":"OK"
        }
    }
    
    report = ""
    
    for tyre,value in result.items():
        report += f"""
        ----------------------------------
        [Tyre REPORT]
        \n
        Tyre : {tyre}
        Severity : {value}
        \n
        Action : {action_take[value]["action"]}
        Priority : {action_take[value]["priority"]}

        ----------------------------------

        """
        
    return report
        


def save_report(report):
    with open("tyre_report.txt","w") as fd:
        fd.write(report)


def print_report(report):
    print(report)



'''
obj = analyze.TyreAnalyzer()

result = obj.check_severity(analyzer.new_sorted_data)
show_report(result)        
'''

# old logic of printing without the (report =) 
        
        # if value == "High":
        #     print(f'''\t\t----------------------------------
        #                     [Tyre REPORT] \n
        #                 Tyre     :  {tyre}
        #                 Severity :  Severity {value} \n
        #                 Action   :  {action_take[value]["action"]}
        #                 Priority :  {action_take[value]["priority"]}
        #             ------------------------------------''')
        # elif ( value == "Medium"):
        #     print(f'''\t\t--------------------------------
        #                 Tyre     :  {tyre}
        #                 Severity :  Severity {value} \n
        #                 Action   :  {action_take[value]["action"]}
        #                 Priority :  {action_take[value]["priority"]}
        #             -----------------------------------''')
        # elif(value == "Good"):
        #     print(f'''\t\t--------------------------------
        #                 Tyre     :  {tyre}
        #                 Severity :  Severity {value} \n
        #                 Action   :  {action_take[value]["action"]}
        #                 Priority :  {action_take[value]["priority"]}
        #             -----------------------------------''')
