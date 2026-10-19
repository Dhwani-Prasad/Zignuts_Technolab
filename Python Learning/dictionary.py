# 2. Create a dictionary-based program to manage contacts. 
#    Take the complex JSON ( mix of list and dictionary ) and destructure it

contact = {}

while True:
  print("\nEnter 1 to Create contact")
  print("Enter 2 to Search contact")
  print("Enter 3 to Delete contact")
  print("Enter 4 to Display contact")
  print("Enter 5 to Exit")

  choice = int(input("Enter your choice : "))
  
  if (choice == 1):
    name = input("Enter name : ")
    phone = input("Enter phone number : ")
    contact[name] = phone
    print("Contact added Successfully")

  elif (choice == 2):
    name = input("Enter name to search : ")
    if name in contact:
      print("Phone:", contact[name])  
    else:
      print("Name not found")

  elif (choice == 3):
    name = input("Enter name to delete : ")
    if name in contact:
        del contact[name]
        print("Contact deleted")
    else:
      print("Name not found")

  elif (choice == 4):
    print(contact)

  elif (choice == 5):
    break

  else:
    print("Enter valid input")