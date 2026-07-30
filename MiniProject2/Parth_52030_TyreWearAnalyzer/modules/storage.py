
import json


class DataStorage:
    
    def save_data(self,data):
        with open("tyre_history.json","w") as fd:
            # fd.write(data)
            json.dump(data,fd,indent=4)
    
    
    def load_data(self):
        with open("tyre_history.json","r") as fd :
            new_data = json.load(fd)
            return new_data


'''

#for testing purpose create fake dictionary :-  
dict_data = {"Car" : "CAR001",
                "front_left" : 1,
                "front_right" : 2,
                "rear_left" : 3,
                "rear_right" : 4
            }


obj = DataStorage()
obj.save_data(data)


# new_data = obj.load_data()
# print(new_data)


# To back to get that data from that file 
new_data = obj.load_data()
print(new_data)

'''


