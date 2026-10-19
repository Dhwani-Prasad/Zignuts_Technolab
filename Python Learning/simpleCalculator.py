# Simple Calculator: Build a CLI-based calculator that supports basic arithmetic operations 
# and handles invalid input gracefully. 


def calculator():
    while True:
        print("\nCalculator")
        print("Enter 1 for Addition")
        print("Enter 2 for Subtraction")
        print("Enter 3 for  Multiplication")
        print("Enter 4 for Division")
        print("Enter 5 for Exit")

        choice = input("Enter your choice: ")

        if choice == "5":
            print("Quit Calculator")
            break

        if choice not in ["1", "2", "3", "4"]:
            print("Enter valid choice")
            continue

        try:
            a = float(input("Enter first number: "))
            b = float(input("Enter second number: "))

            if choice == "1":
                ans = a + b
            elif choice == "2":
                ans = a - b
            elif choice == "3":
                ans = a * b
            elif choice == "4":
                if b == 0:
                    print("Error: Cannot divide by zero.")
                    continue
                ans = a / b

            print("Result:", ans)

        except ValueError:
            print("Enter valid input")


calculator()