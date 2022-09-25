import random
import pandas

#We define the diferent strategies for our players

#0: Always C
def cooperatorStrategy(moves, player):
    return False

#1: Always D
def defectorStrategy(moves, player):
    return True

#2: Tif for Tat
def tftStrategy(moves, player):
    if len(moves) == 0:
        return False
    return moves[len(moves)-1][not player]

#3: Spiteful
def spitefulStrategy(moves, player):
    if len(moves) == 0:
        return False

    if not moves[len(moves)-1][player]:
        if  not moves[len(moves)-1][not player]:
            return False
        return True
    return True

#4: Naive Prober
def naiveProberStrategy(moves, player):
    if len(moves) == 0:
        return False
    if random.random() <= 0.01:
        return True
    return moves[len(moves)-1][not player]

#5: TF2T Strategy
def tf2tStrategy(moves, player):
    if len(moves) <= 1:
        return False
    if not moves[len(moves)-2][not player] and not moves[len(moves)-1][not player]:
        return False
    return True

#6: Random Player
def randomStrategy(moves, player):
    return random.random() <= 0.5

#We create a list with the diferent strategies for our players
strategies = [cooperatorStrategy, defectorStrategy, tftStrategy, spitefulStrategy, naiveProberStrategy, tf2tStrategy, randomStrategy]
#Payoff matrix 
payoffMatrix = [[(4,4),(0,5)],[(5,0),(2,2)]]

#We define the different tournaments that will take place
tournaments = [[0]*5+[1]*5+[2]*5+[3]*5+[4]*5+[5]*5, [6]*15 + [1]*5 + [2]*3 + [0]*5 + [3]*2, [1]*5 + [2]*20 + [5]*2 + [3] + [0] + [4]]

for tournament in tournaments:
    #We store the moves that take place in every individual contests
    moves = [[list() for j in range(len(tournament))] for i in range(len(tournament))]
    #We set the scores in every tournament for the different players to 0
    scores = [[[0,0] for j in range(len(tournament))] for i in range(len(tournament))]
    #We set the TOTAL scores for the different players to 0
    totalScores = [0 for i in range(len(tournament))]

    print('TOURNAMENT STARTS')
    #We iterate over every pair of players in our contest
    for i in range(len(tournament)):    
        for j in range(i+1,len(tournament)):
            #We iterate over the rounds
            for round in range(20):
                #Every player decides its next move
                move = (strategies[tournament[i]](moves[i][j],0), strategies[tournament[j]](moves[i][j],1))
                #We add the latest moves to the list of moves
                moves[i][j].append(move)
                #We increment the scores according to the values in our payoff matrix
                scores[i][j][0] += payoffMatrix[move[0]][move[1]][0]
                scores[i][j][1] += payoffMatrix[move[0]][move[1]][1]
            
            #We update the total scores
            totalScores[i] += scores[i][j][0]
            totalScores[j] += scores[i][j][1]
    #The tournament ends
    print('TOURNAMENTS ENDS, CONTESTS SCORES:')
    namesStrategies = list(map(lambda x: strategies[x].__name__ , tournament))
    df = pandas.DataFrame(scores, namesStrategies, namesStrategies)
    print(df)
    #We save the results in CSV format
    df.to_csv('./results' + str(tournaments.index(tournament)) + '.csv')
    #We sort the competitors according to their scores
    #namesStrategiesSorted = [x for _,x in sorted(zip(totalScores,namesStrategies),reverse=True)]
    #totalScores.sort(reverse=True)
    print('TOTAL SCORES: ')
    #We show the total results
    for i in range(len(tournament)):
       print(strategies[tournament[i]].__name__ + ' -> ' + str(totalScores[i]))

"""
CONCLUSIONS:
In general, the top-performing strategies are Tit for Tat, Spiteful, Tit for 2 Tats and Naive Prober.
The main trait that these strategies have in common is that the player does not defect its opppenent 
until the other one does (except for Naive Prober who defects with a probability of 1%). However, once 
the other player defects, the player starts defecting. At these point, there is main difference among our 
strategies: for Tit for Tat, Tit for 2 Tats and Naive Prober, cooperation can be restablished if the other 
player starts cooperating again. This does not happen for the spiteful strategy, who will defect regardless
of the other player starting to cooperate again. Thus, we say the first set of strategies is forgiving. 
From the results obtained, its not clear which strategy is the best, although the spiteful strategy seems 
to perform well in the contest with many random players.

In the other hand, we see that the most simple strategies (defector and cooperator) do not perform very 
well compared with the other strategies mentioned. In the case of the defector strategy, this may seem odd, 
as it is a dominant strategy for the player. However, cooperation gives greater rewards than defection, 
so strategies which involve some cooperation between players usually lead to higher scores.
"""

