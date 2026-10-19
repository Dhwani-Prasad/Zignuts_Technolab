# 1. Write a python program to find the sum of first N prime numbers. 

n = int(input("Enter a number"))

count = 0
num =2
total = 2

while count < n:
  primeNo = True
  for i in range(2, num):
    if num % i == 0:
      primeNo = False
      break

  if primeNo:
    total += num
    count += 1

  num += 1

print("Sum of first", n, "prime numbers is:", total)