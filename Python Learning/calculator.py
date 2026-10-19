#  3. Write a simple calculator that accepts two numbers and an operator (+, -, *, /) and prints the result. 

n = input("Enter a operation : ")
a = float(input("Enter a : "))
b = float(input("Enter b : "))

if (n == '+'):
  ans = a+b
  print("Answer : ", ans)
elif (n == '-'):
  ans = a-b
  print("Answer : ", ans)
elif (n == '/'):
  ans = a/b
  print("Answer : ", ans)
elif (n == '*'):
  ans = a*b
  print("Answer : ", ans)
else:
  print("Enter valid input")