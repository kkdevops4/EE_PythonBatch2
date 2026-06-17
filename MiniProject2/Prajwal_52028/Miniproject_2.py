import re


#print("="*50)
print("\t DTC FAULT CODE SUMMARY\n")
#print("="*50)
class DTC_Report:
    def __init__(self):
        self.powertrain=[]
        self.chassis=[]
        self.body=[]
        self.network=[]
        self.invalid_code=[]
    def read_file(self,filename):
        pattern= r"^[PCBU]\d{4}$"

        try:
            with open(filename,"r") as file:
                for line in file:
                    code=line.strip().upper()

                    if not code:
                        continue

                    if re.match(pattern,code):
                        if code[0]=="P":
                            self.powertrain.append(code)
                        elif code[0]=="C":
                            self.chassis.append(code)
                        elif code[0]=="B":
                            self.body.append(code)
                        elif code[0]=="U":
                            self.network.append(code)
                    else:
                        self.invalid_code.append(code)

        except FileNotFoundError:
            print("Error:File Not Found")
        
        else:
            print("Code Parsering Started...\n")
            
        finally:
            print("DTC Fault Code Parsering Completed!\n")


    def generate_report(self):
        
        #print("*"*50)
        print("\t Generated OBD Report\n")
        #print("*"*50)
        
        for code in self.powertrain:
            print(f"{code}:Powertrain System Fault")
        print("Powertrain Code Count:",len(self.powertrain))

        print("\n")

        for code in self.chassis:
            print(f"{code}:Chassis System Fault")
        print("Chassis Code Count:",len(self.chassis))

        print("\n")

        for code in self.body:
            print(f"{code}:Body System Fault")
        print("Body Code Count:",len(self.body))

        print("\n")

        for code in self.network:
            print(f"{code}:Network System Fault")
        print("Network Code Count:",len(self.network))

        print("\n")

        for code in self.invalid_code:
            print(f"{code}:Invalid Code")
        print("Count:",len(self.invalid_code))

        print("\n")

        total_valid=(len(self.powertrain)+len(self.chassis)+len(self.body)+len(self.network))
        
        print("Total Valid Code Count:",total_valid)
        print("Total Invalid Code Count:",len(self.invalid_code))


    def save_report(self):
        with open("report.txt","w") as file:
            file.write("Exported Report\n")
            #file.write("="*50)
            file.write(f"\nPowertrain Count:{len(self.powertrain)}\n")
            file.write(f"Chassis Count:{len(self.chassis)}\n")
            file.write(f"Body Count:{len(self.body)}\n")
            file.write(f"Network Count:{len(self.network)}\n")
            #file.write("="*50)
            file.write(f"\nTotal Valid Count:{(len(self.powertrain)+len(self.chassis)+len(self.body)+len(self.network))}\n")
            file.write(f"Total Invalid Count:{len(self.invalid_code)}\n")

def main():
    report=DTC_Report()
    report.read_file("dtc_code.txt")
    report.generate_report()
    report.save_report()


if __name__ == "__main__":
    main()