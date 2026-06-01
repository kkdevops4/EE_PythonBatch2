# Employee Payroll System

employees = []
dept_total = {}

#input from user
n = int(input("Enter number of employees: "))

for i in range(n):

    print("\nEnter details for Employee:")

    name = input("Enter employee name: ")
    emp_id = int(input("Enter employee ID: "))
    department = input("Enter department: ")

    basic_salary = float(input("Enter basic salary: "))
    overtime_hrs = int(input("Enter overtime hours: "))

    employee = {
        'name': name,
        'emp_id': emp_id,
        'department': department,
        'basic_salary': basic_salary,
        'overtime_hrs': overtime_hrs
    }

    employees.append(employee)

# Overtime Function
def overtime(hours):
    overtime_rate = 1000
    return hours * overtime_rate

# Tax calculation
def tax_cal(gross_salary):

    if gross_salary <= 400000:
        return 0

    elif 400000 < gross_salary <= 800000:
        return gross_salary * 0.05

    elif 800000 < gross_salary <= 1200000:
        return gross_salary * 0.10

    elif 1200000 < gross_salary <= 1600000:
        return gross_salary * 0.15

    elif 1600000 < gross_salary <= 2000000:
        return gross_salary * 0.20

    elif 2000000 < gross_salary <= 2400000:
        return gross_salary * 0.25

    else:
        return gross_salary * 0.30

# Calculate salary details
for emp in employees:

    overtime_pay = overtime(emp['overtime_hrs'])

    gross_salary = emp['basic_salary'] + overtime_pay

    tax = tax_cal(gross_salary)

    net_salary = gross_salary - tax

    emp['gross_salary'] = gross_salary
    emp['tax'] = tax
    emp['net_salary'] = net_salary

    if emp['department'] in dept_total:
        dept_total[emp['department']] += net_salary
    else:
        dept_total[emp['department']] = net_salary


# PAYSLIP

def print_payslip(emp):

    print("\nPAYSLIP")
    print("Name               :", emp['name'])
    print("Employee ID        :", emp['emp_id'])
    print("Department         :", emp['department'])
    print("Basic Salary       :", emp['basic_salary'])
    print("Overtime Hours     :", emp['overtime_hrs'])
    print("Gross Salary       :", emp['gross_salary'])
    print("Income Tax         :", emp['tax'])
    print("Net Salary         :", emp['net_salary'])
    print("Department Net Pay :", dept_total[emp['department']])
    print()


print("\nFINAL PAYSLIPS")

for emp in employees:
    print_payslip(emp)

print("\nTOTAL NET PAY PER DEPARTMENT")

for dept, total in dept_total.items():
    print(dept, ":", total)