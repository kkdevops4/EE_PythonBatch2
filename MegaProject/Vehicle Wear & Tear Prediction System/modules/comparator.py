
# Own logic 

def compare(vehicle_value , threshold):
    green = threshold["GREEN"] 
    yellow = threshold["YELLOW"]  
    red = threshold["RED"]

    if ( "-" in green ):
        start , end = green.split("-")
        start = float(start)
        end = float(end)

        if(start <= vehicle_value <=end) :
            return "GREEN"   

    elif ">" in green:
        green_value = green.replace(">", "")
        green_value = float(green_value)

        if vehicle_value > green_value:
            return "GREEN" 

    if ( "-" in yellow ):
        start , end = yellow.split("-")
        start = float(start)
        end = float(end)

        if(start <= vehicle_value <=end) :
            return "YELLOW"    


    if "<" in red :
        red_value = red.replace("<","")
        red_value = (float(red_value))

        if(vehicle_value < red_value) :
            return "RED"    


    elif ">" in red :
        red_value = red.replace(">","")
        red_value = (float(red_value))
        
        if(vehicle_value > red_value) :
            return "RED"    

    # print("INVALID FOUND")
    # print(vehicle_value)
    # print(threshold)
    return "INVALID" 







# Future chages for the gren also 
'''
-> for the future scope the error handeling for (Green)

elif "<" in green:

    green_value = green.replace("<", "")
    green_value = float(green_value)

    if vehicle_value < green_value:
        return "GREEN"

'''





# This is implementation before testing divided in many parts :-

'''
# 
string = "70 - 95"

if '-' in string :
    start,end = (string.split("-"))


start = float(start)
end = float(end)
prfloat(start)

prfloat(type(start))

prfloat(end)
prfloat(type(end))

number = float(input("Enter no between 70-95 : "))
if(start <= number <= end):
    prfloat("Green")
elif(number > end ) : 
    prfloat("RED")
else:
    prfloat("Not Defined...:(")




new_string = ">105"

if ">" in new_string :
    new_string = new_string.replace(">","") 
    new_string = float(new_string)


prfloat("New string : ",new_string)
prfloat(type(new_string))



data = "<30"

if "<" in data :
    data = data.replace("<","")
    data = (float(data))

prfloat("data :" ,data ," \n")
prfloat(type(data))

number = float(input("No checks the requirenment : "))
if number < data :
    prfloat("RED")
else:
    prfloat("Good")

'''







# Another implementation technique given from the AI
'''

def compare(vehicle_value, threshold):

    green = threshold["GREEN"]
    yellow = threshold["YELLOW"]
    red = threshold["RED"]

    # GREEN RANGE (70-95)
    if "-" in green:

        start, end = map(float, green.split("-"))

        if start <= vehicle_value <= end:
            
            return "GREEN"

    # YELLOW RANGE (96-105)
    if "-" in yellow:

        start, end = map(float, yellow.split("-"))

        if start <= vehicle_value <= end:
            
            return "YELLOW"

    # RED RANGE (>105 or <30)
    if ">" in red:

        value = float(red.replace(">", ""))

        if vehicle_value > value:
            
            return "RED"

    if "<" in red:

        value = float(red.replace("<", ""))

        if vehicle_value < value:
            
            return "RED"
        

    return "UNKNOWN"

'''