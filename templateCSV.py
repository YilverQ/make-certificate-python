import csv

with open('Data.csv', newline='') as File:  
    number = 0
    reader = csv.DictReader(File)

    for row in reader:
        number += 1;
        print(row)
        if number == 10:
            break