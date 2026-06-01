cat_1 = []
cat_2 = []
cat_3 = []

while True:
    print("1. Add Expense category wise")
    print("2. Summary of expenses ")
    print("3. Exit ")

    user_input = input("Enter the No. of action you want to perform: ")
    

    if user_input == "1" :
        # cat_1 = []
        # cat_2 = []
        # cat_3 = []
        print("1. category 1")
        print("2. category 2")
        print("3. category 3")

        for_cat = input("Enter the category you want to add expense: ")    
        if for_cat == "1":
            num = int(input("Enter the no. of values to add: "))
            for n in range(num):
                value = int(input("Enter the value to add: "))
                cat_1.append(value)
                # nonlocal cat_1
                print(f"Cat_1 expenses you have add: {cat_1}")
                if sum(cat_1) > 1000:
                     print("WARNING")
                else:
                    continue
        elif for_cat == "2":
            num = int(input("Enter the no. of values to add: "))
            for n in range(num):
                value = int(input("Enter the value to add: "))
                cat_2.append(value)
                # nonlocal cat_1
                print(f"Cat_2 expenses you have add: {cat_2}")
                if sum(cat_2) > 1000:
                     print("WARNING")
                else:
                    continue
        elif for_cat == "3":
            num = int(input("Enter the no. of values to add: "))
            for n in range(num):
                value = int(input("Enter the value to add: "))
                cat_3.append(value)
                # nonlocal cat_1
                print(f"Cat_3 expenses you have add: {cat_3}")
                if sum(cat_3) > 1000:
                     print("WARNING")
                else:
                    continue
        else:
            print("Invalid category chosed!")
    
    elif user_input == "2":
        # print("List of category 1: {type(cat_1)}")
        # print("List of category 2: {cat_2}")
        # print("List of category 3: {cat_3}")
        print(f"Total in Category one: {cat_1} & its total expense is {sum(cat_1)}")
        print(f"Total in Category two: {cat_2} & its total expense is {sum(cat_2)}")
        print(f"Total in Category three: {cat_3} & its total expense is {sum(cat_3)}")
        
    elif user_input == "3":
         break
    else:
         print("Invalid input")