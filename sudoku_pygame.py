import pygame
import sys
from sudoku_logic import SudokuGame, GameThread

# Initialize Pygame
pygame.font.init()
screen = pygame.display.set_mode((500, 675))
screen.fill((255, 255, 255))
pygame.display.set_caption("SudokuApp")
a_font = pygame.font.SysFont("times", 30, "bold")
inc = 500 // 9
x, y = 0, 0
UserValue = 0
IsRunning = True
IsSolving = False
grid = [[0] * 9 for _ in range(9)]

# Start the Pygame game thread
GameThread()
