
import json


class TyreAnalyzer:
    def __init__(self):
        self.result = {}    
        
    def analyze(self):
        with open("tyre_history.json","r") as fd :
            data = json.load(fd) 
            tyre_data = data["tyres"]
            return tyre_data            

            
    def check_severity(self,tyre_data):
        for tyre in tyre_data: #or tyre,value in tyre_data.items() also accept        
            if(tyre[1] > 60): #or value > 60 also work
                # print(tyre[0], " = High")
                value = "High"
            elif(tyre[1] > 30):
                # print(tyre[0]," = Medium")
                value = "Medium"                
            else:
                # print(tyre[0]," = Good")
                value = "Good"
            self.result.update({tyre[0]:value})
        
        return self.result
        

    def sort_data(self,tyre_data):
        new_sorted_data = sorted(tyre_data.items() , key = lambda sorting : sorting[1],reverse=True )
        
        return new_sorted_data
    
    

    



'''

obj = TyreAnalyzer()
tyre_data = obj.analyze()

# print("Before Sorting",tyre_data)
# Sorting lambda Logic for the tyre data 
new_sorted_data = sorted(tyre_data.items() , key = lambda sorting : sorting[1],reverse=True )
# print("After Sorting", new_sorted_data)


result = obj.check_severity(new_sorted_data)
# print(result)

'''
