# Enter names and marks for multiple students, compute averages, assign grades,
#  and print formatted report cards

students = {}

def add_student(students):
    name = input("\nEnter name : ")

    maths = int(input("Enter maths marks : "))
    science = int(input("Enter science marks : "))
    english = int(input("Enter english marks : "))

    subjects = {
        'Maths  ' : maths,
        'Science' : science,
        'English' : english
    }

    students[name] = subjects

    print("Student added Successfully !")

def view_students(students):
    if len(students) == 0:
        print("No students found !")
    else:
        print("\nStudent List")
        for name, subjects in students.items():
            print("\nName :",name)

            for subject, marks in subjects.items():
                print(f"{subject} : {marks}")

def average_mark(students):
    
    name = input("\nEnter student name = ")

    if name in students:

        total = 0

        for marks in students[name].values():
            total = total + marks

        avg = total / len(students[name])

        print(f"{name}'s Average marks =",round(avg,2))
    
    else:
        print("Student not found !")

def calculate_grade(percent):
    if percent >= 90:
        return "A+"
    elif percent >= 80:
        return "A"
    elif percent >= 70:
        return "B+"
    elif percent >= 60:
        return "B"
    elif percent >= 50:
        return "C+"
    elif percent >= 40:
        return "C"
    else:
        return "Fail"
    
def report_card():

    name = input("\nEnter student name = ")
    
    if name in students:
        print("\n-----------------------------")
        print("      Student Report:")
        print("-----------------------------")
        print("Name : ",name)
        print("----------- Marks -----------")
        total = 0

        for subject, marks in students[name].items():
            print(f"{subject}         : {marks}")
            
            total = total + marks

        percent = total / 300 * 100
        grade = calculate_grade(percent)
        print("-----------------------------")
        print("Percentage      =",round(percent,2))
        print("Obatained Grade =",grade)
        print("-----------------------------")
        print("\n")
    else:
        print("Student not found !")
        
while True:
    print("\nStudent Report Card")
    print("1. Add student")
    print("2. View Students")
    print("3. Average")
    print("4. Report Card")
    print("5. Exit")

    choice = int(input("Enter Choice: "))

    match choice :
        case 1:
            add_student(students)
        
        case 2:
            view_students(students)
        
        case 3:
            average_mark(students)

        case 4:
            report_card()

        case 5:
            print("Exiting")
            break

        case _:
            print("invalid choice")

