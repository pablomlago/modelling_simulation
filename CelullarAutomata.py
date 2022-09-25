import pygame
import sys
import numpy as np

#We define the function to update the grid from one generation to other
def updateGrid(grid, gridWidth, gridHeight):
    #Initialize a new grid
    newGrid = [[0 for j in range(gridWidth)] for i in range(gridHeight)]

    #We iterate over the cells of the grid
    for i in range(gridHeight):
        for j in range(gridWidth):
            neighbours = 0
            #We compute the number of neighbours
            for h in range(-1, 2, 1):
                for l in range(-1, 2, 1):
                    if h != 0 or l != 0:
                        neighbours += grid[(i + h) % gridHeight][(j + l) % gridWidth]
            #Rules of evolution
            if grid[i][j] and neighbours >= 2 and neighbours <= 3:
                newGrid[i][j] = grid[i][j]
            elif not grid[i][j] and neighbours == 3:
                newGrid[i][j] = 1
            else:
                newGrid[i][j] = 0

    return newGrid

pygame.init()

#Size of our grid
gridHeight = 60
gridWidth = 80

black=(0,0,0)
white=(255,255,255)
fps = 60

#Patterns to create when pressing
patterns = [[(-1,1),(0,-1),(0,1),(1,0),(1,1)],[(-1,-1),(-1,2),(0,-2),(1,-2),(1,2),(2,-2),(2,-1),(2,0),(2,1)]]

#Set edit mode to false in the beginning
edit = False

#We can pass modify the parameters introducing them by the command line
if len(sys.argv) > 1:
    if sys.argv[1] == '-edit':
        edit = True

dis=pygame.display.set_mode((10*gridWidth,10*gridHeight), 32, pygame.NOFRAME)
pygame.display.set_caption('Game of Life')
 
fpsClock = pygame.time.Clock()


if edit:
    grid = [[0 for j in range(gridWidth)] for i in range(gridHeight)]
    fps = 60
else:
    grid = [[np.random.randint(2) for j in range(gridWidth)] for i in range(gridHeight)]
    fps = 10

game_over = False

selectedPattern = 0
click = False
while not game_over:
    pos = [int(cord/10) for cord in pygame.mouse.get_pos()]
    for event in pygame.event.get():   
        if event.type==pygame.QUIT:
            game_over=True
        if event.type == pygame.MOUSEBUTTONUP:
            click = not edit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_over=True
            if event.key == pygame.K_SPACE:
                selectedPattern = (selectedPattern+1) % len(patterns)
            if event.key == pygame.K_RETURN:
                edit = not edit
                fps = 60 if edit else 10

    for i in range(gridHeight):
        for j in range(gridWidth):
            pygame.draw.rect(dis,(np.random.randint(255),np.random.randint(255),np.random.randint(255)) if grid[i][j] else black,[10*j,10*i,10,10])
    
    pygame.display.update()
    fpsClock.tick(fps)

    #The user can change the state of the grid by clicking
    if edit:
        if pygame.mouse.get_pressed()[0]:
            grid[pos[1]][pos[0]] = 1
        if pygame.mouse.get_pressed()[2]:
            grid[pos[1]][pos[0]] = 0
    else:
        grid = updateGrid(grid, gridWidth, gridHeight)
        if click:
            click = False
            #We update the position clicked with the selected pattern
            if pos is not None:
                for square in patterns[selectedPattern]:
                    grid[(pos[1]+square[0])%gridHeight][(pos[0]+square[1])%gridWidth] = 1

pygame.quit()
quit()