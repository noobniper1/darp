import math,random,time
import matplotlib.pyplot as plt
#Read coordinate file
filename = 'cities.txt' 
city_num = [] #City number
city_location = [] #City coordinates
with open('cities.txt', 'a') as the_file:
    for i in range(1, 26):
        x=int(random.random() * 200)
        y=int(random.random() * 200)
        th=random.randint(8, 18)
        tm=random.randint(0, 59)
        the_file.write('{} {} {} {} {}\n'.format(i, x, y, th, tm))

print("The file was successfully created")
