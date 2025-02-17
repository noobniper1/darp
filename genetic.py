import math,random,time
import matplotlib.pyplot as plt
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
city_count = len(city_num) #Total number of cities
origin = 1 #Set start and end
remain_cities = city_num[:] 
remain_cities.remove(origin)#Cities that change during iteration
remain_count = city_count - 1 #Number of cities changed during iteration
indexs = list(i for i in range(remain_count))
#Calculate the adjacency matrix
dis =[[0]*city_count for i in range(city_count)] #initialization
for i in range(city_count):
    for j in range(city_count):
        if i != j:
            dis[i][j] = math.sqrt((city_location[i][0]-city_location[j][0])**2 + (city_location[i][1]-city_location[j][1])**2)
        else:
            dis[i][j] = 0

def route_mile_cost(route):
    '''
         Calculate the mileage cost of the route
    '''
    mile_cost = 0.0
    mile_cost += dis[0][route[origin-1]-1]#Start from the starting point
    for i in range(remain_count-1):#Path length
        mile_cost += dis[route[i]-1][route[i+1]-1]
    mile_cost += dis[route[-1]-1][origin-1] #To the end
    return mile_cost

#Get the shortest distance in the current neighbor city
def nearest_city(current_city,remain_cities):
    temp_min = float('inf')
    next_city = None
    for i in range(len(remain_cities)):
        distance = dis[current_city-1][remain_cities[i]-1]
        if distance < temp_min:
            temp_min = distance
            next_city = remain_cities[i]
    return next_city

def greedy_initial_route(remain_cities):
    '''
         The greedy algorithm is used to generate the initial solution: starting from the first city, find the city with the shortest distance from it and mark it,
         Then continue to find and mark the city with the shortest distance from the second city until all the cities are marked.
         Finally return to the first city (starting city)
    '''
    cand_cities = remain_cities[:]
    current_city = origin
    initial_route = []
    while len(cand_cities) > 0:
        next_city = nearest_city(current_city,cand_cities) #Find the nearest city and its distance
        initial_route.append(next_city) #Add the next city to the route list
        current_city = next_city #Update current city
        cand_cities.remove(next_city) #Update unsequenced cities
    return initial_route

#Natural selection, survival of the fittest
def selection(population):
    '''
         Select parent individuals
    '''
    M = population_size
    parents = []
    tabu_list = []
    tabu_length = 5
    for i in range(M):
    #to do: tabu search
        #if random.random() < (1 - i/M):
        #    parents.append(population[i])
    return parents
def CPX(parent1,parent2):
    '''
         Cross-breeding: The mixed parents of CX and PX produce two offspring
    '''
    cycle = []
    start = parent1[0]
    cycle.append(start)
    end = parent2[0]
    while end != start:
        cycle.append(end)
        end = parent2[parent1.index(end)]
    child = parent1[:]
    cross_points = cycle[:]
    if len(cross_points) < 2 :
        cross_points = random.sample(parent1,2)
    k = 0
    for i in range(len(parent1)):
        if child[i] in cross_points:
            continue
        else:
            for j in range(k,len(parent2)):
                if parent2[j] in cross_points:
                    continue
                else:
                    child[i] = parent2[j]
                    k = j + 1
                    break   
    return child

#Mutations
def mutation(children,mutation_rate):
    '''
         Offspring mutation
    '''
    for i in range(len(children)):
        if random.random() < mutation_rate:
            child = children[i]
            new_child = child[:]
            index = sorted(random.sample(indexs,2))
            L = index[1] - index[0] + 1
            for j in range(L):
                new_child[index[0]+j] = child[index[1]-j]
            path = [origin] + child + [origin]
            a,b = index[0] + 1,index[1] + 1
            d1 = dis[path[a-1]-1][path[a]-1] + dis[path[b]-1][path[b+1]-1]
            d2 = dis[path[a-1]-1][path[b]-1] + dis[path[a]-1][path[b+1]-1]
            if d2 < d1:
                children[i] = new_child

    return children

def get_best_current(population):
    '''
         Sort the individuals of the population according to mileage, and return the best individuals in the current population and their mileage
    '''
    graded = [[route_mile_cost(x),x] for x in population]
    graded = sorted(graded)
    population = [x[1] for x in graded]
    return graded[0][0],graded[0][1],population

population_size = 100 #Population
mutation_rate = 0.2 #Mutation probability
def main(iter_count):
    #Initialize population
    population = [greedy_initial_route(remain_cities)]
    # population = []
    for i in range(population_size-1):
        #Randomly generate individuals
        individual  = remain_cities[:]
        random.shuffle(individual)
        population.append(individual)
    mile_cost,result,population = get_best_current(population)
    record = [mile_cost] #Record the optimal value of each reproduction
    i = 0
    while i < iter_count:
        #Select breeding population
        parents = selection(population)
        #Crossbreeding
        target_count = population_size - len(parents) #The number of reproduction required (to maintain the size of the population)
        children = []
        while len(children) < target_count:
            parent1,parent2 = random.sample(parents,2)
            child1 = CPX(parent1,parent2)
            child2 = CPX(parent2,parent1)
            children.append(child1)
            children.append(child2)
        #Parent Variation
        parents = mutation(parents,1)
        #Offspring variation
        children = mutation(children,mutation_rate)
        #Update population
        population = parents + children
        #Update breeding results
        mile_cost,result,population = get_best_current(population) 
        record.append(mile_cost) #Record the optimal solution after each reproduction
        i += 1
    route = [origin] + result + [origin]
    return route,mile_cost,record

def fig():
    time_start = time.time()
    N = 1000 #Evolution times
    satisfactory_solution,mile_cost,record = main(N)
    time_end = time.time()
    time_cost = time_end - time_start
    print('time cost:',time_cost)
    print("Optimize mileage cost: %d" %(int(mile_cost)))
    print("Optimization Path:\n",satisfactory_solution)
    #Drawing a route map
    X = []
    Y = []
    for i in satisfactory_solution:
        x = city_location[i-1][0]
        y = city_location[i-1][1]
        X.append(x)
        Y.append(y)
    plt.plot(X,Y,'-o')
    plt.title("satisfactory solution of TS:%d"%(int(mile_cost)))
    plt.show()
    #Draw iterative process diagram
    A = [i for i in range(N+1)]#Abscissa
    B = record[:] #Y-axis
    plt.xlim(0,N)
    plt.xlabel('Number of evolution',fontproperties="SimSun")
    plt.ylabel('Path mileage',fontproperties="SimSun")
    plt.title("solution of GA changed with evolution")
    plt.plot(A,B,'-')
    plt.show()
    return mile_cost,time_cost

fig()
   
# record1 = [0]*10
# record2 = [0]*10
# for i in range(10):
#     record1[i],record2[i] = fig()
# print(min(record1))
# print(sum(record1)/10)
# print(record1)
# R = 10
# Mcosts = [0]*R
# Tcosts = [0]*R
# for j in range(R):
#     Mcosts[j],Tcosts[j] = fig()
# AM = sum(Mcosts)/R #Average mileage
# AT = sum(Tcosts)/R #Average time
# print("Minimum mileage:",min(Mcosts))
# print("Average mileage:",AM)
# print('mileage:\n',Mcosts)
# print("Average time:",AT)

