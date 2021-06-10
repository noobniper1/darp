# -*- coding: utf-8 -*-
"""
Taboo search algorithm solveTSPProblem
 Random0,100) 2D plane generation20Point
 Distance minimization
"""
import math
import random
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']    # Add this allows graphics to display Chinese

 # Calculate the path distance, that is, the evaluation function
def calFitness(line,dis_matrix):
    dis_sum = 0
    dis = 0
    for i in range(len(line)):
        if i<len(line)-1:
            dis = dis_matrix.loc[line[i],line[i+1]]# Calculate distance
            dis_sum = dis_sum+dis
        else:
            dis = dis_matrix.loc[line[i],line[0]]
            dis_sum = dis_sum+dis
    return round(dis_sum,1)


def traversal_search(line,dis_matrix,tabu_list):
         #            
    traversal = 0# Search
    traversal_list = []# Storage Local Search Generation,Also act as partial contraindication table
    traversal_value = []# Storage partial solution correspondence path distance
    while traversal <= traversalMax:
        pos1,pos2 = random.randint(0,len(line)-1),random.randint(0,len(line)-1)#      
                 # Copy the current path and exchange the generated path
        new_line = line.copy()
        new_line[pos1],new_line[pos2]=new_line[pos2],new_line[pos1]
        new_value = calFitness(new_line,dis_matrix)# Current path distance
                 # New generation path is not in the global taboo table and partial contraindications, for effective search, otherwise continue searching
        if (new_line not in traversal_list) & (new_line not in tabu_list):
            traversal_list.append(new_line)
            traversal_value.append(new_value)
            traversal += 1
            
    return min(traversal_value),traversal_list[traversal_value.index(min(traversal_value))]


def greedy(CityCoordinates,dis_matrix):
    '''Greedy strategy structure initial solution'''
         #     Dis_matrix
    dis_matrix = dis_matrix.astype('float64')
    for i in range(len(CityCoordinates)):dis_matrix.loc[i,i]=math.pow(10,10)
    line = []# Initialization
    now_city = random.randint(0,len(CityCoordinates)-1)# Randomly generate a city
    line.append(now_city)# Add current city to the path
    dis_matrix.loc[:,now_city] = math.pow(10,10)# Update the distance matrix, has been taken out of the city
    for i in range(len(CityCoordinates)-1):
        next_city = dis_matrix.loc[now_city,:].idxmin()# Distance nearest city
        line.append(next_city)# Add into the path
        dis_matrix.loc[:,next_city] = math.pow(10,10)# Update Distance Matrix
        now_city =  next_city # Update the current city
        
    return line
    
    
 #Please path diagram
def draw_path(line,CityCoordinates):
    x,y= [],[]
    for i in line:
        Coordinate = CityCoordinates[i]
        x.append(Coordinate[0])
        y.append(Coordinate[1])
    x.append(x[0])
    y.append(y[0])
    
    plt.plot(x, y,'r-', color='#4169E1', alpha=0.8, linewidth=0.8)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()


if __name__ == '__main__':
    
    #Read coordinate file
    filename = 'cities.txt' 
    city_num = [] #City number
    city_location = [] #City coordinates
    with open(filename, 'r') as f:
        datas = f.readlines()[:]
    for data in datas:
        data = data.split()
        city_num.append(int(data[0]))
        x = float(data[1])
        y = float(data[2])
        city_location.append((x,y))#City coordinates
    
    CityCoordinates = city_location[:]

         # Parameter
    CityNum = 25# City quantity
    MinCoordinate = 0# 2D coordinate minimum value
    MaxCoordinate = 200# 2D coordinate maximum
    
    #TSParameter
    tabu_limit = 50 #Taboo length, this value should be less than(CityNum*(CityNum-1)/2）
    iterMax = 200#  
    traversalMax = 100# Each generation partial search number
    
    tabu_list = []  #     table
    tabu_time = []  #  
    best_value = math.pow(10,10)#Ghine initial value, store the best solution
    best_line = []# Storage optimal path
    
    
         # Randomly generate urban data,Urban serial number0,1，2,3...
#    CityCoordinates = [(random.randint(MinCoordinate,MaxCoordinate+1),random.randint(MinCoordinate,MaxCoordinate+1)) for i in range(CityNum)]
 #   ＃ CityCoordinates = [(88, 16),(42, 76),(5, 76),(69, 13),(73, 56),(100, 100),(22, 92),(48, 74),(73, 46),(39, 1),(51, 75),(92, 2),(101, 44),(55, 26),(71, 27),(42, 81),(51, 91),(89, 54),(33, 18),(40, 78)]

         # Calculate the distance between the city
    dis_matrix = pd.DataFrame(data=None,columns=range(len(CityCoordinates)),index=range(len(CityCoordinates)))
    for i in range(len(CityCoordinates)):
        xi,yi = CityCoordinates[i][0],CityCoordinates[i][1]
        for j in range(len(CityCoordinates)):
            xj,yj = CityCoordinates[j][0],CityCoordinates[j][1]
            dis_matrix.iloc[i,j] = round(math.sqrt((xi-xj)**2+(yi-yj)**2),2)
    
         # # Initialization,Random
    # line = list(range(len(CityCoordinates)));random.shuffle(line)
    # value = calFitness(line,dis_matrix)#    
         #      
    line = greedy(CityCoordinates,dis_matrix)
    value = calFitness(line,dis_matrix)#    
    
    
         # Storage current optimal
    best_value,best_line = value,line
    draw_path(best_line,CityCoordinates)
    best_value_list = []
    best_value_list.append(best_value)
         # Update taboo table
    tabu_list.append(line)
    tabu_time.append(tabu_limit)
    
    itera = 0
    while itera <= iterMax:
        new_value,new_line = traversal_search(line,dis_matrix,tabu_list)
        if new_value < best_value:#          
            best_value,best_line = new_value,new_line # Update the best solution
            best_value_list.append(best_value)
        line,value = new_line,new_value # Update the current solution
        
                 # Update taboo table
        tabu_time = [x-1 for x in tabu_time]
        if 0 in tabu_time:
            tabu_list.remove(tabu_list[tabu_time.index(0)])
            tabu_time.remove(0)
        
        tabu_list.append(line)
        tabu_time.append(tabu_limit)
        itera +=1
    
         #      
    print(best_line)
         #Please path diagram
    draw_path(best_line,CityCoordinates)

