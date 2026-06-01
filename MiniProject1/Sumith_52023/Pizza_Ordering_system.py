# Pizza order system 
#  Choose size, crust, and toppings from a menu, compute the bill with tax, and print an order ticket.

# Control Flow	Strings	Lists & Tuples	Dicts & Sets	Functions

def calculate_bill(base_price,topping_list):
    total_topping_cost=0
    for topping in topping_list:
        if topping=="Pepperoni":
            total_topping_cost=total_topping_cost+50
        elif topping=="Mushrooms":
            total_topping_cost=total_topping_cost+30
        elif topping=="Extra cheese":
            total_topping_cost=total_topping_cost+40
        elif topping=="Olives":
            total_topping_cost=total_topping_cost+20
        elif topping=="Pineapple":
            total_topping_cost=total_topping_cost+40
        
    tax_rate=0.18
    subtotal=base_price+total_topping_cost
    tax_amount=subtotal*tax_rate
    final_bill=subtotal+tax_amount

    return final_bill,subtotal,tax_amount,total_topping_cost


print("Welcometo the Pizza Ordering system\n")
print("---------------------------------------")

base_price=0
crust_name=""
size=int(input("Please choose th size of your pizza\n 1.Small(Rs.150)\n2.medium(Rs.250)\n3.large(Rs.350)\n"))
if size==1:
    base_price=150
    size_name="Small"
elif size==2:
    base_price=250
    size_name="Medium"
elif size==3:
    base_price=350
    size_name="Large"

else:
    print("Invalid Size selected !!! Default size set to medium")
    base_price=250
    size_name="Medium"
    size=2



crust=int(input("Enter the crust option for your pizza\n1.Hand-tossed(Rs.0)\n2.Stuffed crust(Rs.50)\n3.Flatbread(Rs.30)\n"))
if crust==1:
    crust_name="Hand-tossed"
elif crust==2:
    crust_name="Stuffed crust"
    base_price=base_price+50
elif crust==3:
    crust_name="Flatbread"
    base_price=base_price+30
else:
    crust_name="Hand-tossed"
    print("Invalid crust selected !!! Default crust selescted as Hand-tossed")


selected_toppings=[]

print("Choose your toppings(1 for Yes , 0 for No):")

add_pepproni=int(input("Do you want Pepproni? (1. for Yes, 0 for No)"))
if add_pepproni==1:
    selected_toppings.append("Pepproni")

add_mushrooms=int(input("Do you want mushrooms? (1. for Yes , 0 for No):"))
if add_mushrooms==1:
    selected_toppings.append("Mushrooms")

add_cheese=int(input("Do you want to add extra cheese? (1 for Yes , 0 for No)"))
if add_cheese==1:
    selected_toppings.append("Extra cheese")

add_olives=int(input("Do you want olives ?(1 for yes , 0 for No)"))
if add_olives==1:
    selected_toppings.append("Olives")

add_pineapple=int(input("Do you want pineapple ? (1 for Yes , 0 for No)"))
if add_pineapple==1:
    selected_toppings.append("Pineapple")

final_bill,subtotal,tax_amount,topping_cost=calculate_bill(base_price,selected_toppings)

print("\n--------------------------------------------------------------")
print("                YOUR ORDER TICKET")
print("---------------------------------------------------------------")
print(f"Size:{size_name}")
print(f"Crust:{crust_name}")

print("\n Toppings Selected:")
if len(selected_toppings)==0:
    print(" -None")
else:
    for topping in selected_toppings:
        print(f"  -{topping}")

print("--------------------------------------------------------")

print(f"Base Price + Crust:          {base_price}")
print(f"Total Toppings Cost:         {topping_cost}")
print(f"Subtotal:                    {subtotal}")
print(f"Tax(18% GST):                {tax_amount:.2f}")
print("-------------------------------------------------------")
print(f"TOTAL BILL:                   {final_bill}")
print("------------------------------------------------------")
print("Thank you for ordering !!!")

