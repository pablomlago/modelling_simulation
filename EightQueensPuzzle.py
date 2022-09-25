import random
import sys

#Size of our population
N=1000
#Probability of gene mutation
mutationProbability = 0.01
#Maximum number of iterations
maxIterations = 1000000

#We can set the parameters by command line
if len(sys.argv) == 4:
    N = int(sys.argv[1])
    mutationProbability = float(sys.argv[2])
    maxIterations = int(sys.argv[3])

#List with all the genomes of individuals
population=[[random.randint(1,8) for j in range(8)] for i in range(N)]

#Function to compute the fitness of a phenotype
def computeFitnessPhenotype(phenotype):
    #The maximum number of attacks is 28
    fitness = 28
    #We check for every queen pair if they attack between themselves
    for i in range(8):
        for j in range(i+1, 8):
            #Check attacks in rows, antidiagonal and diagonal
            fitness -= phenotype[i] == phenotype[j] or phenotype[i]+i == phenotype[j]+j or phenotype[i]-i == phenotype[j]-j
    #We return the fitness of the phenotype
    return fitness

#We create maxIterations generations at most
for t in range(maxIterations):
    #We compute the fitness score for every phenotype in our population
    fit = [computeFitnessPhenotype(population[i]) for i in range(N)]

    #We check if there is a solution in our population
    for i in range(N):
        #A value of 28 for fitness indicates a solution
        if fit[i] == 28:
            print('------ SOLUTION FOUND ------')
            print('Iteracions: ' + str(t))
            print('Solution: ' + str(population[i]))
            #We exit from the program
            sys.exit()
    
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
        rn = random.randint(0,sum[N-1]-1)
        for j in range(N):
            #We will choose the index of the leftmost subinterval which contains rn
            if(rn < sum[j]):
                mating.append(population[j])
                break

    #Now, we will apply the crossover operator to our population  
    newPopulation=list()
    for i in range(0,N,2):
        #We generate the croosover site randomly
        crossoverSite = random.randint(0,8)
        #Our new population will contain the result of crossovering the phenotypes in our mating pool
        newPopulation.append(mating[i][:crossoverSite]+mating[i+1][crossoverSite:])
        newPopulation.append(mating[i+1][:crossoverSite]+mating[i][crossoverSite:])

    #Finally we will apply the mutation operator
    #We iterate over every gene the phenotypes of our population
    for i in range(N):
        for j in range(8):
            #We generate a random number from a uniform distribution [0, 1]
            mutationRandom = random.random()
            if mutationRandom <= mutationProbability:
                #The selected gene mutates
                newPopulation[i][j] = random.randint(1,8)
    
    #We update our population
    population=newPopulation

#We reach this point if the maxIterations was reached
print('------ MAX ITERATIONS REACHED ------')
#We show the current population and its fitness values
for i in range(N):
    print(str(population[i]) + ' -> ' + str(fit[i]))