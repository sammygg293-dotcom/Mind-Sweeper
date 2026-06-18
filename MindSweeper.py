import random

def gridGen(gridSpace, empty, bombs):
    gridRange = range(0, gridSpace)
    gridgrid = []
    unrevealed = []
    for space in range(0, gridSpace):
        grid = [empty]*gridSpace
        Ugrid = ["\u25A0"]*gridSpace
        gridgrid.append(grid)
        unrevealed.append(Ugrid)
    bombsPlanted = 0
    bomb = "X"
    middle = gridSpace // 2
    while bombsPlanted <= bombs:
        index1 = random.choice(gridRange)
        index2 = random.choice(gridRange)
        while gridgrid[index1][index2] == bomb or (index1 == index2 == middle):
            index1 = random.choice(gridRange)
            index2 = random.choice(gridRange)        
        gridgrid[index1][index2] = bomb
        leftToRight = [-1, 0, 1]
        for addition1 in leftToRight:
            for addition2 in leftToRight:
                try:
                    nextToBomb = gridgrid[index1 + addition1][index2 + addition2]
                    if nextToBomb == empty:
                        gridgrid[index1 + addition1][index2 + addition2] = "1"
                    else:
                        gridgrid[index1 + addition1][index2 + addition2] = str(int(gridgrid[index1 + addition1][index2 + addition2]) + 1)
                except:
                    continue
        bombsPlanted+=1
    return gridgrid, unrevealed
def coord_Val(coords, gridspace):
    splitCoords = coords.split("/")
    if len(splitCoords) != 2:
        return False
    try:
        for axis in splitCoords:
            if not (0 < int(axis) <= gridspace):
                return False
    except:
        return False
    return True
def zeroMap(playerScreen, bombfield, gridSpace, empty):
    tempScreen = playerScreen
    leftToRight = [-1, 0, 1]
    zeroFilled = False
    addOn1 = [-1, 0, 0, 1]
    addOn2 = [0, -1, 1, 0]
    while not zeroFilled:
        zeroFilled = True
        yInd = 0
        fillArr = []
        for Ygrid in tempScreen:
            xInd = 0
            for item in Ygrid:
                if item == empty:
                    addOnIndex = 0
                    while addOnIndex < 4:
                        y, x = yInd + addOn1[addOnIndex], xInd + addOn2[addOnIndex]
                        if y < 0 or y > gridSpace - 1:
                            addOnIndex+=1
                            continue
                        elif x < 0 or x > gridSpace - 1:
                            addOnIndex+=1
                            continue
                        if tempScreen[y][x] == "\u25A0":
                            fillArr.append([y,x])
                            zeroFilled = False
                        addOnIndex+=1
                xInd+=1
            yInd+=1
        for revealChart in fillArr:
            coords1, coords2 = revealChart[0], revealChart[1]
            playerScreen[coords1][coords2] = bombfield[coords1][coords2]
    return playerScreen
def gridFormat(grid, gridSpace):
    Yxis = 0
    grid_biggestSpace = len(str(gridSpace))
    numberPlaces = []
    numberRange = range(1, gridSpace + 1)
    for count in numberRange:
        numberPlaces.append([])
    for number in numberRange:
        numberIndex = grid_biggestSpace - 1
        stringNum = str(number)
        numberlen = len(stringNum) - 1
        numberPlace = 0
        while numberIndex >= 0:
            if numberIndex <= numberlen:
                numberPlaces[numberIndex].append(stringNum[numberPlace])
                numberPlace+=1
            else:
                numberPlaces[numberIndex].append("0")
            numberIndex-=1
    numberIndex = grid_biggestSpace - 1
    while numberIndex >= 0:
        print("   "+" ".join(numberPlaces[numberIndex]))
        numberIndex-=1
    print("   "+"-"*(gridSpace*2-1))
    for line in grid:
        Yxis+=1
        Y_Str = str(Yxis)
        gridYSpace = "0"*(grid_biggestSpace-len(Y_Str))
        print(gridYSpace+Y_Str+"|"+ " ".join(line) + "|")
def inputs():
    print("Enter co-ordinates in the format X coordinate/Y coordinate")
    print("X and Y co-ordinates can be found on top and right of grid")
    newCoords = input("Please enter your selection co-ordinates here: ")
    while not coord_Val(newCoords, gridSpace):
        print("Invalid input, please input two numbers between 0 and "+str(gridSpace))
        print("Enter co-ordinates in the format X coordinate/Y coordinate")
        print("X and Y co-ordinates can be found on top and right of grid")
        newCoords = input("Please enter your selection co-ordinates here: ")
    newCoords = newCoords.split("/")
    Ycoord, Xcoord = int(newCoords[1]) - 1, int(newCoords[0]) - 1
    flagStatus = "flag"
    if playerScreen[Ycoord][Xcoord] == flag:
        flagStatus = "unflag"
    flagged = input(f"Do you want to {flagStatus} this position? Y/N: ").upper()
    while flagged != "Y" and flagged != "N":
        print("Please type Y or N")
        flagged = input("Do you want to {flagStatus} this position? Y/N: ").upper()
    return Ycoord, Xcoord, flagged, flagStatus
def countFlags(bombfield, bombs):
    total = 0
    for bombArr in bombfield:
        total+=bombArr.count("\u25C0")
    print(f"Total bombs defused: {total}/{bombs}")
    if total != bombs:
        print("You lose")
    else:
        print("You win")

gameCreate = True
while gameCreate == True:
    print("Your input will be used to determine how big the grid is generated.")
    print("Numbers three or under will not be accepted.")
    print("Please type the size of the grid below.")
    sizeInput = input("Type size here: ")
    while not sizeInput.isdigit() or int(sizeInput) <= 3:
        print("\nPlease input size in full, whole numbers under three.")
        sizeInput = input("Type size here: ")

    gridSpace = int(sizeInput)
    empty = " "

    flags = gridSpace * round(gridSpace / 10)
    if flags < 1:
        flags = 1
    bombs = flags
    bombfield, playerScreen = gridGen(gridSpace, empty, bombs)
    gridFormat(playerScreen, gridSpace)
    print(f"Flags left: {flags}")
    exploded = False
    flag = "\u25C0"
    while exploded == False:
        enterLoop = True
        Ycoord, Xcoord, flagged, flagStatus = inputs()
        while bombfield[Ycoord][Xcoord] == playerScreen[Ycoord][Xcoord]:
            print("Placement already revealed as safe, try another. \n")
            Ycoord, Xcoord, flagged, flagStatus = inputs()
        behindResult = bombfield[Ycoord][Xcoord]
        if flagged == "Y":
            if flagStatus == "flag":
                target = flag
                flags-=1
                if behindResult == "X":
                    bombfield[Ycoord][Xcoord] = flag
            else:
                target = "\u25A0"
                flags+=1
                if behindResult == flag:
                    bombfield[Ycoord][Xcoord] = "X"
        else:
            if flagStatus == "flag":
                target = behindResult
            
        playerScreen[Ycoord][Xcoord] = target
        if target == empty:
            playerScreen = zeroMap(playerScreen, bombfield, gridSpace, empty)
        print("\n\n\n\n")
        gridFormat(playerScreen, gridSpace)
        print(f"Flags left: {flags}")
        if target == "X" or flags == 0:
            countFlags(bombfield, bombs)
            exploded = True
        elif bombs == 0:
            print("You win")
            gridFormat(bombfield, gridSpace)
        if playerScreen[Ycoord][Xcoord] == flag:
            flagStatus = "unflag"
    continuation = input(f"Do you want to play again? Y/N: ").upper()
    while continuation != "Y" and flagged != "N":
        print("Please type Y or N")
        continuation = input(f"Do you want to play again? Y/N: ").upper()
    if continuation == "N":
        gameCreate == False
    else:
        print("\n\n\n\n")
#"  "
#"\u2591\u2591"
#"\u2588\u2588"
