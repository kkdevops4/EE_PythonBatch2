# -------------------------------
# Read Existing Vehicle Records
# -------------------------------

file = open("vehicles.txt", "r")

data = file.read()

print("----- Existing Vehicle Records -----")
print(data)

file.close()


# -------------------------------
# Append New Vehicle Record
# -------------------------------

file = open("vehicles.txt", "a")

file.write("\nVIN5678,Amit,Verna,2025")

file.close()

print("\nNew Vehicle Record Appended Successfully")


# -------------------------------
# Read Updated Vehicle Records
# -------------------------------

file = open("vehicles.txt", "r")

updated_data = file.read()

print("\n----- Updated Vehicle Records -----")
print(updated_data)

file.close()