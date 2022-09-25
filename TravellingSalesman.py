import random
import math
import sys

#Size of our population
N=10
#Probability of gene mutation
mutationProbability = 0.01
#Maximum number of iterations without improvement
maxIterations = 100
#Maximum weight of a path between cities
maxWeight = 100
#Score in previous iteration
tempScore = None

#We can set the parameters by command line
if len(sys.argv) == 4:
    N = int(sys.argv[1])
    mutationProbability = float(sys.argv[2])
    maxIterations = int(sys.argv[3])

#We let the user introduce the number of cities
C = int(input('Enter the number of cities: '))
#We initialize the coordinates of the cities to [0,0]
citiesCoordinates = [[0.,0.] for i in range(C)]
#We ask the user for the coordinates of the cities
print('Enter the coordinates of the cities')
for i in range(C):
    print('City ' + str(i))
    citiesCoordinates[i][0] = float(input('X: '))
    citiesCoordinates[i][1] = float(input('Y: '))

#We initialize a matrix with the distances between cities
graph = [[math.sqrt((citiesCoordinates[i][0]-citiesCoordinates[j][0])**2 + (citiesCoordinates[i][1]-citiesCoordinates[j][1])**2) for j in range(C)] for i in range(C)]

#List with all the genomes of individuals
#We generate random permutations of [1, ..., C-1]. We suppose that we start and finish in city 0
population=[random.sample(list(range(1,C)), C-1) for i in range(N)]

#Function to compute the costs of the paths encoded in every phenotype of our population
def computeCostPopulation(population, graph):
    #We initialize to 0 the costs of the paths encoded in each phenotype
    cost = [0. for i in range(N)]
    #We iterate over the phenotype and compute the costs of the paths
    for i in range(N):
        cost[i] += graph[0][population[i][0]]
        for j in range(1,C-1):
            cost[i] += graph[population[i][j-1]][population[i][j]]
        cost[i] += graph[population[i][C-2]][0]
    #We return the cost of the paths encoded in our population
    return cost

#This counter will hold the number of iterations without changes in the score of the paths of our population
iterations = 0
#We will iterate until there is no improvement in the scores of the elements of our population
while True:
    #We compute the cost of the paths encoded in every phenotype of our population
    cost = computeCostPopulation(population, graph)
    #We compute the value of fitness for every element in our population
    fit = [max(cost)-cost[i] for i in range(N)]

    #We check if the number of iterations without improvements has been excedeed
    if tempScore is None:
        #If this is the first iteration, we store the minimum cost in the first iteration
        tempScore = min(cost)
    else:
        #We check if the cost obtained is less than for the population in the previous iterations
        if tempScore >= min(cost):
            #Otherwise, we increase the counter
            iterations += 1
            #If the maximum number of iterations without improvement is reached we break from the loop
            if(iterations >= maxIterations):
                break
        else:
            #We update the minimum cost and reset the counter
            tempScore = min(cost)
            iterations = 0
    
    #We will use roulette wheel selection for choosing the individuals for our mating pool

    #Firstly, we will compute F
    #We will use a array containing the partial sums for the elements in our fitness array
    sum = fit.copy()
    for i in range(1,N):
        sum[i] += sum[i-1]

    #Using randomly generated numbers, we will choose the individuals for our mating pool
    mating = list()
    for i in range(N):
        #We generate a random number in the interval [0, F)
        rn = random.random()*sum[N-1]
        for j in range(N):
            #We will choose the index of the leftmost subinterval which contains rn
            if(rn <= sum[j]):
                mating.append(population[j])
                break

    #Now, we will apply the crossover operator to our population  
    newPopulation=list()
    for i in range(0,N,2):
        #We generate the croosover sites randomly
        interval = [random.randint(0,C-1), random.randint(0,C-1)]
        #We sort the extremes of our interval
        interval.sort()
        #Initialization of offspring
        offspring = [0]*(C-1)
        #We add the first subset of cities in the same position as in mating[i]
        offspring[interval[0]:interval[1]] = mating[i][interval[0]:interval[1]]
        #We filter the cities that we have already added to our offspring
        filteredList = list(filter(lambda x: x not in offspring[interval[0]:interval[1]], mating[i+1]))
        #We add the rest of cities in the remaining positions
        t = 0
        for j in range(len(filteredList)):
            if t >= interval[0] and t < interval[1]:
                t = interval[1]
            offspring[t] = filteredList[j]
            t += 1
        #We add the new offspring to the new population
        newPopulation.append(offspring.copy())
        #We add the first subset of cities in the same position as in mating[i+1]
        offspring[interval[0]:interval[1]] = mating[i+1][interval[0]:interval[1]]
        #We filter the cities that we have already added to our offspring
        filteredList = list(filter(lambda x: x not in offspring[interval[0]:interval[1]], mating[i]))
        #We add the rest of cities in the remaining positions
        t = 0
        for j in range(len(filteredList)):
            if t >= interval[0] and t < interval[1]:
                t = interval[1]
            offspring[t] = filteredList[j]
            t += 1
        #We add the new offspring to the new population
        newPopulation.append(offspring.copy())

    #Finally we will apply the mutation operator
    #We iterate over every gene the phenotypes of our population
    for i in range(N):
        for j in range(C-1):
            #The mutation occurs with a probability of mutationProbability
            mutationRandom = random.random()
            #We will swap to randomly chosen genes
            if mutationRandom <= mutationProbability:
                #We generate randomly the index to swap
                swapIndex = random.randint(0, C-2)
                #The selected gene mutates
                newPopulation[i][j], newPopulation[i][swapIndex] = newPopulation[i][swapIndex], newPopulation[i][j]
    
    #We update our population
    population=newPopulation

#We reach this point if the maxIterations was reached
print('------ MAX ITERATIONS REACHED ------')
#We show the element of the current population with the highest value for fitness
minIndex = cost.index(min(cost))
print(str([0]+population[minIndex]+[0]) + ' -> ' + str(cost[minIndex]))