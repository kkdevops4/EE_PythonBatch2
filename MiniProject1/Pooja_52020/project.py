#print("hello")
 #Enter names and marks for multiple students, compute averages, assign grades, and print formatted report cards.

student = {}

def calculate_grade(average):
    if average >= 80:
        return 'A'
    elif average >= 50 and average < 80:
        return 'B'
    else:
        return 'C' 

num = int(input("Enter number of students: "))

for i in range(num):
    print(f"\nEnter details for student {i + 1}")
    name = input("Enter name of student: ")
    phy = int(input("Enter marks of Physics: "))
    maths = int(input("Enter marks of Maths: "))
    english = int(input("Enter marks of English: "))

    total = phy + maths + english
    average = total / 3
    grade = calculate_grade(average)

   # print("grade:",grade)
    student[name] = {
        "Physics": phy,
        "Maths": maths,
        "English": english,
        "Average": average,
        "Grade": grade
    }

def print_report_card(student_name):
 for name, details in student.items():
    if student_name == name:
        print(f"\nName: {student_name}")
        print("Marks and Grades :")
      #  print(f"Average: {details['Average']:.2f}")
        for subject, marks in details.items():
           print(f"{subject}: {marks}")

      
for name in student:
    student_name = input("Enter the name of the student to view report card: ")

    if student_name in student:
        print_report_card(student_name)
    else:
        print("Student not found.")

