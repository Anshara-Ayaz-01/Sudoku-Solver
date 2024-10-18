import pygame
import sys
import random
from pygame_widgets.button import Button

# Define global variables
IsRunning = True
IsSolving = False
grid = [[0] * 9 for _ in range(9)]
x = 0
y = 0
UserValue = 0

# Initialize Pygame
pygame.font.init()
screen = pygame.display.set_mode((500, 675))
screen.fill((255, 255, 255))
pygame.display.set_caption("SudokuApp")
a_font = pygame.font.SysFont("times", 30, "bold")
inc = 500 // 9

def RandomlyGenerateHints(difficulty):
    global grid

    # Generate hints based on the difficulty level
    if difficulty == 'easy':
        hints_to_generate = 15
    elif difficulty == 'medium':
        hints_to_generate = 9
    elif difficulty == 'hard':
        hints_to_generate = 6
    else:
        raise ValueError("Invalid difficulty level")

    # Reset the grid to an empty state
    grid = [[0] * 9 for _ in range(9)]

    # Create a list of all possible (row, col) pairs
    all_positions = [(i, j) for i in range(9) for j in range(9)]

    # Randomly fill the hints
    while hints_to_generate > 0 and all_positions:
        # Randomly select a position from the remaining list
        row, col = random.choice(all_positions)
        value = random.randint(1, 9)

        if IsUserValueValid(grid, row, col, value):
            grid[row][col] = value
            hints_to_generate -= 1

        # Remove the selected position from the list
        all_positions.remove((row, col))

def DrawGrid():
    # Draw the lines
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                # filling the non-empty cells
                pygame.draw.rect(screen, (204, 102, 153), (i * inc, j * inc, inc + 1, inc + 1))
                # inserting the default values
                text = a_font.render(str(grid[i][j]), True, (0, 0, 0))
                screen.blit(text, (i * inc + 15, j * inc + 10))
    # Draw lines horizontally and vertically to form grid
    for i in range(10):
        if i % 3 == 0:
            width = 10  # every 3 small boxes -> thicker line
        else:
            width = 5
        pygame.draw.line(screen, (0, 0, 0), (i * inc, 0), (i * inc, 500), width)  # vertical
        pygame.draw.line(screen, (0, 0, 0), (0, i * inc), (500, i * inc), width)  # horizontal

def SolveGrid(gridArray, i, j):
    global IsSolving

    # Find an empty cell to start solving
    find = FindEmptyCell(gridArray)
    if not find:
        return True  # If there's no empty cell, the Sudoku is solved

    i, j = find

    for V in range(1, 10):  # Trying values from 1 to 9 inclusive
        if IsUserValueValid(gridArray, i, j, V):
            gridArray[i][j] = V

            if SolveGrid(gridArray, i, j):
                return True

            gridArray[i][j] = 0  # Backtrack if the solution wasn't correct

        # Clear the screen and redraw the grid
        screen.fill((255, 255, 255))
        DrawGrid()
        DrawSelectedBox()
        DrawModes()
        DrawSolveButton()
        pygame.display.update()
        pygame.time.delay(20)

    return False

def FindEmptyCell(gridArray):
    for i in range(9):
        for j in range(9):
            if gridArray[i][j] == 0:
                return i, j
    return False

def IsUserValueValid(m, i, j, v):
    for ii in range(9):
        if m[i][ii] == v or m[ii][j] == v:
            return False

    box_i = (i // 3) * 3
    box_j = (j // 3) * 3
    for row in range(box_i, box_i + 3):
        for col in range(box_j, box_j + 3):
            if m[row][col] == v:
                return False

    return True

def DrawSelectedBox():
    for i in range(2):
        pygame.draw.line(screen, (0, 0, 255), (x * inc, (y + i) * inc), (x * inc + inc, (y + i) * inc), 5)
        pygame.draw.line(screen, (0, 0, 255), ((x + i) * inc, y * inc), ((x + i) * inc, y * inc + inc), 5)

def InsertValue(Value):
    grid[int(x)][int(y)] = Value
    text = a_font.render(str(Value), True, (0, 0, 0))
    screen.blit(text, (x * inc + 15, y * inc + 15))

def IsUserWin():
    for i in range(9):
        for j in range(9):
            if grid[int(i)][int(j)] == 0:
                return False
    return True

def DrawModes():
    TitleFont = pygame.font.SysFont("times", 20, "bold")
    AttributeFont = pygame.font.SysFont("times", 20)
    screen.blit(TitleFont.render("Game Settings", True, (0, 0, 0)), (15, 505))
    screen.blit(AttributeFont.render("C: Clear", True, (0, 0, 0)), (30, 530))
    screen.blit(TitleFont.render("Modes", True, (0, 0, 0)), (15, 555))
    screen.blit(AttributeFont.render("E: Easy", True, (0, 0, 0)), (30, 580))
    screen.blit(AttributeFont.render("A: Average", True, (0, 0, 0)), (30, 605))
    screen.blit(AttributeFont.render("H: Hard", True, (0, 0, 0)), (30, 630))

def DrawSolveButton():
    button = Button(
        screen, 350, 600, 120, 50, text='Solve',
        fontSize=20, margin=20,
        inactiveColour=(0, 0, 255),
        pressedColour=(0, 255, 0), radius=20,
        onClick=lambda: SolveGrid(grid, 0, 0))
    button.listen(pygame.event.get())
    button.draw()

def DisplayMessage(Message, Interval, Color):
    screen.blit(a_font.render(Message, True, Color), (220, 530))
    pygame.display.update()
    pygame.time.delay(Interval)
    screen.fill((255, 255, 255))
    DrawModes()
    DrawSolveButton()

def SetGridMode(Mode):
    global grid
    screen.fill((255, 255, 255))
    DrawModes()
    DrawSolveButton()
    if Mode == 0:
        grid = [[0] * 9 for _ in range(9)]
    elif Mode == 1:
        RandomlyGenerateHints('easy')
    elif Mode == 2:
        RandomlyGenerateHints('medium')
    elif Mode == 3:
        RandomlyGenerateHints('hard')

def SetMousePosition(p):
    global x, y
    if p[0] < 500 and p[1] < 500:
        x = p[0] // inc
        y = p[1] // inc

def AutoSolve(gridArray, i, j):
    if not FindEmptyCell(gridArray):
        return True  # If there's no empty cell, the Sudoku is solved

    i, j = FindEmptyCell(gridArray)

    for V in range(1, 10):  # Trying values from 1 to 9 inclusive
        if IsUserValueValid(gridArray, i, j, V):
            gridArray[i][j] = V

            if AutoSolve(gridArray, i, j):
                return True

            gridArray[i][j] = 0  # Backtrack if the solution wasn't correct

        pygame.event.pump()  # Called once every loop
        DrawGrid()
        pygame.display.update()
        pygame.time.delay(20)

    return False

def AutoSolveGame():
    global grid, IsSolving
    IsSolving = True
    AutoSolve(grid, 0, 0)
    IsSolving = False

def HandleEvents():
    global x, y, IsSolving, UserValue
    events = pygame.event.get()
    for event in events:
        # Quit the game window
        if event.type == pygame.QUIT:
            global IsRunning
            IsRunning = False
            sys.exit()
        # Get the mouse position to insert number
        if event.type == pygame.MOUSEBUTTONDOWN:
            SetMousePosition(pygame.mouse.get_pos())
        if event.type == pygame.KEYDOWN:
            if not IsSolving:
                if event.key == pygame.K_LEFT:
                    x -= 1
                if event.key == pygame.K_RIGHT:
                    x += 1
                if event.key == pygame.K_UP:
                    y -= 1
                if event.key == pygame.K_DOWN:
                    y += 1
                if event.key == pygame.K_1:
                    UserValue = 1
                if event.key == pygame.K_2:
                    UserValue = 2
                if event.key == pygame.K_3:
                    UserValue = 3
                if event.key == pygame.K_4:
                    UserValue = 4
                if event.key == pygame.K_5:
                    UserValue = 5
                if event.key == pygame.K_6:
                    UserValue = 6
                if event.key == pygame.K_7:
                    UserValue = 7
                if event.key == pygame.K_8:
                    UserValue = 8
                if event.key == pygame.K_9:
                    UserValue = 9
                if event.key == pygame.K_c:
                    SetGridMode(0)
                if event.key == pygame.K_e:
                    SetGridMode(1)
                if event.key == pygame.K_a:
                    SetGridMode(2)
                if event.key == pygame.K_h:
                    SetGridMode(3)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        AutoSolveGame()

def DrawUserValue():
    global UserValue, IsSolving, grid, x, y  # Ensure these variables are defined in the global scope

    if UserValue > 0:
        if IsUserValueValid(grid, x, y, UserValue):
            if grid[y][x] == 0:  # Adjusted indices to [y][x] for Sudoku grid
                InsertValue(UserValue)
                UserValue = 0
                if IsUserWin():
                    IsSolving = False
                    DisplayMessage("YOU WON!!!!", 5000, (0, 255, 0))
        else:
            DisplayMessage("Incorrect Value", 500, (255, 0, 0))
            UserValue = 0

def InitializeComponent(difficulty='easy'):
    DrawGrid()
    DrawSelectedBox()
    DrawModes()
    DrawSolveButton()
    RandomlyGenerateHints(difficulty)
    pygame.display.update()

def DrawSolveButton():
    global IsRunning, grid, IsSolving
    button = Button(
        screen, 350, 600, 120, 50, text='Solve',
        fontSize=20, margin=20,
        inactiveColour=(0, 0, 255),
        pressedColour=(0, 255, 0), radius=20,
        onClick=lambda: SolveGrid(grid, 0, 0)
    )
    button.draw()

# Modify the GameThread function
def GameThread(difficulty='easy'):
    InitializeComponent(difficulty)
    while IsRunning:
        HandleEvents()
        DrawGrid()
        DrawSelectedBox()
        DrawUserValue()
        DrawSolveButton()  # Draw the solve button without the random button
        pygame.display.update() 



def InitializeRandomGame():
    global IsSolving, IsRunning, grid

    # Reset variables and fill the grid with random hints
    IsSolving = False
    IsRunning = True
    grid = [[0] * 9 for _ in range(9)]
    RandomlyGenerateHints('medium')  # You can adjust the difficulty as needed

    # Start the game loop
    GameThread()

# Add the following line at the end of your code to initialize the random game.
# InitializeRandomGame()

# if __name__ == '__main__':
#     pygame.font.init()
#     screen = pygame.display.set_mode((500, 675))
#     screen.fill((255, 255, 255))
#     pygame.display.set_caption("SudokuApp")
#     a_font = pygame.font.SysFont("times", 30, "bold")
#     inc = 500 // 9
#     x = 0
#     y = 0
#     UserValue = 0
#     IsRunning = True
#     IsSolving = False

#     #     # Specify the difficulty level ('easy', 'medium', or 'hard')
#     #     difficulty_level = 'easy'

#     #     InitializeComponent(difficulty_level)
#     #     GameThread(difficulty_level)

#     while IsRunning:
#         HandleEvents()
#         DrawGrid()
#         DrawSelectedBox()
#         DrawUserValue()
#         pygame.display.update()
InitializeRandomGame()

if __name__ == '__main__':
    GameThread() 