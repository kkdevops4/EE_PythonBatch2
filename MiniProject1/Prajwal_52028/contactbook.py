'''

Prajwal Phalke 
Problem Statement: Store contacts with phone, email, and group tags; 
search by name or group and export a group list.

'''


#By using Hardcore Data:While using hardcore data then adding new details 

'''
contactbook={
    "Rohan":{
        "Phone":"0000000000",
        "Email":"rohan@outlook.com",
        "Group":"Office"
    },
    "Saurabh":{
        "Phone":"1111111111",
        "Email":"saurabh@outlook.com",
        "Group":"Office"
    },
     "Rushikesh":{
        "Phone":"2222222222",
        "Email":"ruhsikesh@outlook.com",
        "Group":"Office"
    },
    "Virat":{
        "Phone":"3333333333",
        "Email":"virat@yahoo.com",
        "Group":"Sportclub"
    },
     "Jasprit":{
        "Phone":"4444444444",
        "Email":"jasprit@yahoo.com",
        "Group":"Sportclub"
    },
     "Hardik":{
        "Phone":"5555555555",
        "Email":"hp@yahoo.com",
        "Group":"Sportclub"
    },
     "Parth":{
        "Phone":"6666666666",
        "Email":"parth@edag.com",
        "Group":"Friends"
    },
     "Sumeet":{
        "Phone":"7777777777",
        "Email":'sumeet@edag.com',
        "Group":"Friends"
    },
     "Vedant":{
        "Phone":"8888888888",
        "Email":"vedant@edag.com",
        "Group":"Friends"
    },
     "Ram":{
        "Phone":"9999999999",
        "Email":"vedant@gmail.com",
        "Group":"Friends"
    },
    "Aruna":{
        "Phone":"123456789",
        "Email":"aruna@gmail.com",
        "Group":"Family"
    },
    "Kashma":{
        "Phone":"987654321",
        "Email":"kshama@gmail.com",
        "Group":"Family"
    },
}

'''

#With using user input data in memory 

contactbook={}

while True:
    print("\n Welcome to ContactBook!\n")
    print("\n What Are You Want To Do?\n")
    print("\n1.Add Contact\n2.View all contacts\n3.Search by Name\n4.Search by Group\n5.Export gorup contact\n6.Exit")
    
    choice=int(input("Enter Your Choice:"))

    if(choice==1):
        name=input("Enter Name of New Contact:").lower()
        if name in contactbook:
            print("Contact Already Exist!")
        else:
            phone=int(input("Enter Phone Number:"))
            email=input("Enter Email-ID of Contact:")
            group=input("Enter Group to Save Contact:")
            print("Contact Saved Successfully!")

            contactbook[name]={
            "Phone":phone,
            "Email":email,
            "Group":group
            }
            print(contactbook)
        
    elif(choice==2):
        print(contactbook)

    elif(choice==3):
        name=input("Search by Name:").lower()
        found=False
        for key,values in contactbook.items():
            if key.lower()==name:
                print(key,values)
                found=True
                break
        if not found:
                print("Contact not found!")

    elif(choice==4):
        group=input("Search by Group:").lower()
        found=False
        for key,values in contactbook.items():
            if values["Group"].lower()==group:
                print(key,values)
                found=True
        if not found:
                print("Contact Not Found!")

    elif(choice==5):
        f=open("contact.txt","+a")
        data=f.write(str(contactbook))
        #print("\nWarning\n Creating .txt file for store contactbook data again press 5 for exporting data\n")
        print("Data Exprted to contact.txt file!")

    elif(choice==6):
        print("You Are Exited!")
        break

    else:
        print("You Choose Wrong Option.")
        break
    

