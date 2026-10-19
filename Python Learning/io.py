# 4. Create a program to read a CSV file and print its content.

import csv

with open("subject.csv", "r") as f:
    reader = csv.reader(f)

    for row in reader:
        print(row)