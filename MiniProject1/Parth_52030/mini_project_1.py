'''
Task manager 

Add tasks with priority and due date, mark them complete, and filter pending vs finished tasks.

'''

enter = input("\tPlease Enter to show my project....!!")
if(enter == ""):
    print("\n\t\t----------- Task manager ------------- \n")



tasks = []


def add_task():
    i = len(tasks)+1
    dict_d1 = {}
    
    while True:
        name = input("Enter Task Name : ")
        if name != "":
            break

        print("Task Name Cannot Be Empty")
        
    while True:
        priority = input("Enter Priority (High/Medium/Low) : ").title()

        if priority in ["High", "Medium", "Low"]:
            break
        print("Invalid Priority")
    
    date = input("Enter Due Date (dd/mm/yy) : ")
    dict_d1.update({"ID" : i , "Task Name" : name , "Priority" : priority , "Due Date" : date , "Status" : "Pending"})
    tasks.append(dict_d1)
    print("Task Added Successfully....:) ")
        

def view_all_task():
    for i in tasks:
        print(f'''
                ID        : {i['ID']}
                Task Name : {i['Task Name']}
                Priority  : {i['Priority']}
                Due Date  : {i['Due Date']}
                Status    : {i['Status']}  ''')
        
    if(len(tasks)==0):
        print("No Tasks Available")


def mark_task():
    for i in tasks:
        print(f" ID : {i['ID']} ")
    
    task_id = int(input("Enter Task ID : "))

    for i in tasks:
        if(task_id == i["ID"]):
            if(i["Status"] == "Pending"):
                i["Status"] = "Completed"
                print(f"{task_id} This Task Marked As Completed successfully....:) ")                
                break
            elif(i["Status"] == "Completed"):
                print(f"{task_id} This Task Already Completed")
                break
    else:
        print(f"{task_id} : Invalid Task ID...:( ")


def pending_task():
    flag = False
    for i in tasks:
        if(i["Status"] == "Pending"):
            print(f'''
                    ID        : {i['ID']}
                    Task Name : {i['Task Name']}
                    Priority  : {i['Priority']}
                    Due Date  : {i['Due Date']}
                    Status    : {i['Status']}  ''')
            flag = True 
        
    if(flag == False):    
        print(" No More Pending Tasks Found....:) ")



def complete_task():
    flag =  False
    for i in tasks:
        if(i["Status"] == "Completed"):
            print(f'''
                    ID        : {i['ID']}
                    Task Name : {i['Task Name']}
                    Priority  : {i['Priority']}
                    Due Date  : {i['Due Date']}
                    Status    : {i['Status']}  ''')    
            flag = True
    if(flag == False):
        print("No Completed Tasks Found....:) ")



def exit_fun():
    print("Thank You For Using Recipe Manager......:) ")



while True:
    ch = int(input('''
                1) Add Task
                2) View All Tasks
                3) Mark Task Complete
                4) Show Pending Tasks
                5) Show Completed Tasks
                6) Exit
                
                Enter your choice  : '''))
            
    match ch:
        case 1 : 
            print("Add Task")
            add_task()
        case 2:
            print("View All Tasks") 
            view_all_task()           
        case 3:
            print("Mark Task Complete")
            mark_task()
        case 4:
            print("Show Pending Tasks") 
            pending_task()
        case 5:
            print("Show Completed Tasks") 
            complete_task()
        case 6:
            print("Exit")
            exit_fun()
            break
        case _:
            print("Invalid Choice please enter Valid choice.....:( ")



