# 1. Write a program to reverse a string without using built-in methods. 


text = input("Enter a string: ")
reverse = ""

for ch in text:
    reverse = ch + reverse

print("Reversed string:", reverse)