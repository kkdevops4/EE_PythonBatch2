from random import randint


class TyreDataGenerator:
    
    def __init__(self):
        self.car_no = 1 
        # print("Tyre Data Generator will be started...!!")

    def generate_reading(self):
        dict_data = ({"vehicle"   : f"CAR{self.car_no}",
                    "tyres" : {
                    "front_left"  : randint(10,90),
                    "front_right" : randint(10,90),
                    "rear_left"   : randint(10,90),
                    "rear_right"  : randint(10,90),
                    }
                    })        
        self.car_no+=1
        return dict_data
            




# Testing individual model :- 

# obj = TyreDataGenerator()

# for i in range(5):
#     value=obj.generate_reading()
#     list_data.append(value)
#     print(value)
    
# print("\n list \n")    
# print(list_data)


    
