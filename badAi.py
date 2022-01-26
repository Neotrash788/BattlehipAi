import pygame
import math
from sys import exit

# Setup
pygame.init()

fps = 10
gridW = 10
gridH = 10
tileSize = 30
currentShipRot = 'h'

clock = pygame.time.Clock()
screen = pygame.display.set_mode((800, 400))

background_surf = pygame.surface.Surface((800, 400))
background_surf.fill((100, 100, 100))
background_rect = background_surf.get_rect(topleft=(0, 0))

# Tile Class

shipLib = {
    1: 5,
    2: 4,
    3: 3,
    4: 3,
    5: 2
}


class tile(pygame.sprite.Sprite):
    def posToCords(self, cords, guess):
        return (cords[0]*tileSize + (tileSize*(gridW + 2)), cords[1]*tileSize) if guess else (cords[0]*tileSize, cords[1]*tileSize)

    def __init__(self, pos, guess=False):
        super().__init__()
        self.hit = False
        self.sunk = False
        self.isShip = False
        self.shipId = None
        self.image = pygame.surface.Surface(
            (tileSize, tileSize), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 255))
        self.rect = self.image.get_rect(topleft=self.posToCords(pos, guess))

    def setAlpha(self, col):
        self.image.fill((0, 0, 0, col))

    def flipAlpha(self):
        if self.isShip:
            self.image.fill((0, 0, 0, 255))
            self.isShip = False
        else:
            self.image.fill((255, 0, 0, 255))
            self.isShip = True

    def hover(self, bool):
        if not self.isShip:
            if bool:
                self.image.fill((255, 0, 0, 100))
            else:
                self.image.fill((0, 0, 0, 255))

    def setColour(self, col):
        self.image.fill(col)

    def gotHit(self):
        self.hit = True
        ai.remaining -= 1
        shipLib[self.shipId] -= 1
        if shipLib[self.shipId] <= 0:
            self.sunk = True
            ai.preferedDirection = ['v', 'h']
            for i in range(len(remaningShips)-1):
                if remaningShips[i] == self.shipId:
                    remaningShips.pop(i)


# Logic Class
class Logic():
    def __init__(self):
        self.previewPlacement_prev = [None]

    def genGrid(self):
        global grid, tiles
        tiles = pygame.sprite.Group()
        grid = []
        for row in range(gridH):
            for col in range(gridW):
                grid.append(tile((col, row)))
        tiles.add(grid)

    def genAiGrid(self):
        global guesses, aiGrid
        guesses = pygame.sprite.Group()
        aiGrid = []
        for row in range(gridH):
            for col in range(gridW):
                aiGrid.append(tile((col, row), True))
        guesses.add(aiGrid)

    def xyToTilesPos(self, pos):
        return pos[0] + pos[1] * gridW if pos[0] <= gridW - 1 and pos[1] <= gridH - 1 else None

    def newValue(self, pos, value):
        grid[self.xyToTilesPos(pos)].setAlpha(value)

    def mousePosToGridPos(self, pos):
        return self.xyToTilesPos((math.floor(pos[0]/tileSize), math.floor(pos[1]/tileSize)))

    def invertRotation(self):
        global currentShipRot
        currentShipRot = 'v' if currentShipRot == 'h' else 'h'

    def setShip(self, pos):
        global currentShip
        if currentShipRot == 'h':
            for i in range(currentShipSize):
                if grid[pos+i].isShip == True:
                    print('Ships Cannot Overlap')
                    return None
            else:
                for i in range(currentShipSize):
                    grid[pos+i].flipAlpha()
                    grid[pos+i].isShip = True
                    grid[pos+i].shipId = shipLib[currentShip]
                    aiGrid[pos + i].shipId = currentShip
                currentShip += 1
                startingShips.pop(0)
        else:
            for i in range(currentShipSize):
                if grid[pos + (gridW * i)].isShip == True:
                    print('Ships Cannot Overlap')
                    return None
            else:
                for i in range(currentShipSize):
                    grid[pos + (gridW * i)].flipAlpha()
                    grid[pos + (gridW * i)].isShip = True
                    grid[pos + (gridW * i)].shipId = shipLib[currentShip]
                    aiGrid[pos + (gridW * i)].shipId = currentShip
                currentShip += 1
                startingShips.pop(0)

    def validPosition(self, pos, rot, size):
        if rot == 'h':
            row = math.floor(pos/gridW)
            for i in range(size):
                if math.floor((pos+i)/gridW) != row:
                    return False
            else:
                return True
        else:
            for i in range(size):
                if pos + (gridW * i) > gridH*gridW-1:
                    return False
            else:
                return True

    def previewPlacement(self, pos):
        if pos == None:
            return None
        if pos != self.previewPlacement_prev[0]:
            for i in self.previewPlacement_prev[1:]:
                grid[i].hover(False)
            self.previewPlacement_prev = [pos]

            if currentShipRot == 'h':
                if self.validPosition(pos, currentShipRot, currentShipSize):
                    for i in range(currentShipSize):
                        grid[pos+i].hover(True)
                        self.previewPlacement_prev.append(pos+i)
            else:
                if self.validPosition(pos, currentShipRot, currentShipSize):
                    for i in range(currentShipSize):
                        grid[pos + (gridW * i)].hover(True)
                        self.previewPlacement_prev.append(pos + (gridW * i))

    def placeShip(self):
        global setup, currentShipSize
        if logic.validPosition(pos, currentShipRot, currentShipSize):
            self.setShip(pos)
            if len(startingShips) >= 1:
                currentShipSize = shipLib[currentShip]
            else:
                setup = False
                ai.bruteForce()
        else:
            print('This Possition Is Outside The Board')

    def aiValidPlacement(self, pos, rotation, Len):
        if self.validPosition(pos, rotation, Len):
            if rotation == 'h':
                for i in range(Len):
                    if aiGrid[pos+i].hit == 'miss':
                        return False
                else:
                    return [pos+i for i in range(Len)]
            else:
                for i in range(Len):
                    if aiGrid[pos + (gridW * i)].hit == 'miss':
                        return False
                else:
                    return [pos + (gridW * i) for i in range(Len)]
        else:
            return False


class Ai():
    def __init__(self):
        self.hits = []
        self.preferedDirection = ['h', 'v']
        self.guessus = 0
        self.remaining = sum(startingShips)
        self.hitBias = 60000

    def biasHits(self):
        print(self.hits)
        for i in self.hits:

            if shipLib[aiGrid[i[1]].shipId] <= 0:
                self.hits = []
                return []

        arr = []
        for position in self.hits:
            pos = position[1]
            # Horizontals
            row = math.floor(pos/gridW)
            for ii in remaningShips:
                for i in range(-1, ii+1):
                    if math.floor((pos + i - 1) / gridW) != row:
                        continue
                    else:
                        arr.append(['h', pos + i - 1])
                        if math.floor((pos - i) / gridW) == row and pos - i >= 0 and pos - i < gridH*gridW:
                            arr.append(['h', pos - i])

            # verticlals
            for i in remaningShips:
                for i in range(-1, ii+1):
                    if pos + (gridW*(i-1)) >= gridH*gridW:
                        continue
                    else:
                        arr.append(['v', pos + (gridW*(i-1))])

                        if pos - (gridW * (i-1)) >= 0:
                            if pos - (gridW * (i-1)) < gridH * gridW:
                                arr.append(['v', pos - (gridW * (i-1))])

        print(f'Hit Biasis -> {arr}')
        return arr

    def bruteForce(self):
        self.guessus += 1
        chance = [0 for i in range(gridW*gridH)]
        # Horizontals
        for shipSize in remaningShips:
            for row in range(gridH):
                for col in range(gridW):
                    if logic.aiValidPlacement((row * gridW) + col, 'h', shipSize) != False:
                        for i in logic.aiValidPlacement((row * gridW) + col, 'h', shipSize):
                            chance[i] += 1
        # Verticals
        for shipSize in remaningShips:
            for row in range(gridH):
                for col in range(gridW):
                    if logic.aiValidPlacement((row * gridW) + col, 'v', shipSize) != False:
                        for i in logic.aiValidPlacement((row * gridW) + col, 'v', shipSize):
                            chance[i] += 1

        for i in self.biasHits():
            if i[0] in self.preferedDirection:
                chance[i[1]] *= self.hitBias
            else:
                chance[i[1]] *= math.floor(self.hitBias/30000)

        for i in range(len(chance)):
            if aiGrid[i].hit == True:
                chance[i] = 0

        # THIS WILL MAKE A STRONG BIAS TO THE TOP LEFT AND NEGITAVE BIAS TO BOTTOM RIGHT, TO REMOVE THIS BIAS MAKE IT CHOOSE FROM THE TOP CHANCE VALUES AT RANDOM NOT JUST THE FIRST ONE (for i in chance...)
        heighest = [0, 0]
        for i in range(len(chance)):
            if chance[i] > heighest[1]:
                heighest = [i, chance[i]]

        for i in range(gridW*gridH):
            if aiGrid[i].hit:
                pass
                # aiGrid[i].setAlpha((math.floor(255/heighest[1]))*chance[i])#Replace this with pass to show hits and misses
            else:
                aiGrid[i].setAlpha((math.floor(255/heighest[1]))*chance[i])
        print(
            f'Ai made a predicition of space({heighest[0]}) with a confadance of ({heighest[1]})/({sum(chance)}) -> ({(heighest[1]/sum(chance))*100}%)')
        prediction = heighest[0]
        if grid[prediction].shipId == None:
            aiGrid[prediction].setColour((0, 0, 255, 255))
            aiGrid[prediction].hit = 'miss'
        else:
            print('HIT!')
            aiGrid[prediction].setColour((255, 0, 0, 255))
            aiGrid[prediction].gotHit()

            for i in self.biasHits():
                if i[1] == prediction:
                    self.preferedDirection = ['v'] if i[0] == 'v' else ['h']
                    break

            print(f'PREFERD DIRECTION -> {self.preferedDirection}')

            if len(self.hits) == 0:
                self.hits.append((aiGrid[prediction].shipId, prediction))
            if self.remaining <= 0:
                print(f'Ai finnished with {self.guessus} moves')
                exit()


startingShips = [5, 4, 3, 3, 2]
remaningShips = [5, 4, 3, 3, 2]
ai = Ai()


# Final Setup
logic = Logic()
logic.genGrid()
logic.genAiGrid()
setup = True
currentShip = 1
currentShipSize = startingShips[0]

while True:
    # Event Loop
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

            if setup:
                if event.key == pygame.K_r:
                    logic.invertRotation()
            else:
                if event.key == pygame.K_SPACE:
                    ai.bruteForce()

        if event.type == pygame.MOUSEMOTION:
            pos = logic.mousePosToGridPos(pygame.mouse.get_pos())
            if setup:
                logic.previewPlacement(pos)

        # Left Click
        if pygame.mouse.get_pressed()[0]:
            pos = logic.mousePosToGridPos(pygame.mouse.get_pos())
            if pos != None and not clicked:
                clicked = True

                if setup:
                    logic.placeShip()

        # Right click
        if pygame.mouse.get_pressed()[2]:
            pos = logic.mousePosToGridPos(pygame.mouse.get_pos())
            if pos != None and not clicked:
                clicked = True

                if setup:
                    pass

        if not pygame.mouse.get_pressed()[0] and not pygame.mouse.get_pressed()[2]:
            clicked = False

    # Update

    # Render
    screen.blit(background_surf, background_rect)
    tiles.draw(screen)
    guesses.draw(screen)
    # Update
    pygame.display.update()
    clock.tick(fps)
