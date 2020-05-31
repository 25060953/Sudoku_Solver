import pygame
import time
import sys
from random import sample


def difficulty():
    pygame.init()
    pygame.font.init()

    run = True
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Difficulty")

    button_easy = pygame.Rect(20, 40, 210, 50)  # creates a rect object size and placement in window
    button_med = pygame.Rect(20, 100, 210, 50)
    button_hard = pygame.Rect(20, 160, 210, 50)
    button_expert = pygame.Rect(20, 220, 210, 50)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos  # gets mouse position

                # checks if mouse position is over the button

                if button_easy.collidepoint(mouse_pos):
                    empties = 40
                    run = False
                elif button_med.collidepoint(mouse_pos):
                    empties = 50
                    run = False
                elif button_hard.collidepoint(mouse_pos):
                    empties = 55
                    run = False
                elif button_expert.collidepoint(mouse_pos):
                    empties = 60
                    run = False

            screen.fill(bg)

            easy_button = pygame.draw.rect(screen, (211, 211, 211), button_easy)
            medium_button = pygame.draw.rect(screen, (211, 211, 211), button_med)
            hard_button = pygame.draw.rect(screen, (211, 211, 211), button_hard)
            expert_button = pygame.draw.rect(screen, (211, 211, 211), button_expert)

            font = pygame.font.SysFont("Times New Roman", 25, True)
            text = font.render("Select a Difficulty:", 1, (0, 0, 0))
            screen.blit(text, (30, 5))

            font = pygame.font.SysFont("Times New Roman", 35, True)
            text = font.render("Easy", 1, (0, 0, 0))
            screen.blit(text, (85, 45))

            font = pygame.font.SysFont("Times New Roman", 35, True)
            text = font.render("Medium", 1, (0, 0, 0))
            screen.blit(text, (60, 105))

            font = pygame.font.SysFont("Times New Roman", 35, True)
            text = font.render("Hard", 1, (0, 0, 0))
            screen.blit(text, (80, 165))

            font = pygame.font.SysFont("Times New Roman", 35, True)
            text = font.render("Expert", 1, (0, 0, 0))
            screen.blit(text, (70, 225))

            pygame.display.update()
            clock.tick(fps)

    return empties
    pygame.quit()


def empty_blocks(mode):
    if mode == 2:
        base = 3
        side = base * base

        # produces a valid baseline solution pattern
        def pattern(r, c): return (base * (r % base) + r // base + c) % side

        def shuffle(s): return sample(s, len(s))

        rBase = range(base)
        rows = [g * base + r for g in shuffle(rBase) for r in shuffle(rBase)]
        cols = [g * base + c for g in shuffle(rBase) for c in shuffle(rBase)]
        nums = shuffle(range(1, base * base + 1))

        # produce random board using randomized baseline pattern
        board_rand = [[nums[pattern(r, c)] for c in cols] for r in rows]

        squares = side * side
        empties = difficulty()
        for p in sample(range(squares), empties):
            board_rand[p // side][p % side] = 0

    else:
        board_rand = [[0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0]]
    return board_rand


pygame.init()
pygame.font.init()

run = True
clock = pygame.time.Clock()
fps = 60
size = [250, 280]
bg = [255, 255, 255] # screen colour
mode = 0
filled = []

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Puzzle Mode")

button_own = pygame.Rect(20, 40, 210, 50)  # creates a rect object size and placement in window
button_rand = pygame.Rect(20, 100, 210, 50)

while run:
    for event in pygame.event.get():

        screen.fill(bg)

        own_button = pygame.draw.rect(screen, (211, 211, 211), button_own)
        rand_button = pygame.draw.rect(screen, (211, 211, 211), button_rand)

        font = pygame.font.SysFont("Times New Roman", 25, True)
        text = font.render("Select a Puzzle Mode:", 1, (0, 0, 0))
        screen.blit(text, (10, 5))

        font = pygame.font.SysFont("Times New Roman", 25, True)
        text = font.render("Own Puzzle", 1, (0, 0, 0))
        screen.blit(text, (60, 50))

        font = pygame.font.SysFont("Times New Roman", 25, True)
        text = font.render("Random Puzzle", 1, (0, 0, 0))
        screen.blit(text, (45, 110))

        if event.type == pygame.QUIT:
                run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos  # gets mouse position

            # checks if mouse position is over the button

            if button_own.collidepoint(mouse_pos):
                board_rand = empty_blocks(1)
                run = False
            elif button_rand.collidepoint(mouse_pos):
                board_rand = empty_blocks(2)
                run = False

        pygame.display.update()
        clock.tick(fps)

pygame.quit()

pygame.init()
pygame.font.init()
new = []

class Grid:

    board = board_rand


    def __init__(self, rows, cols, width, height, window):
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.board[i][j],i,j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.update_model()
        self.selected = None
        self.window = window

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place(self, val):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()

            if valid(self.model, val, (row,col)): # and self.solve() removed, because after I enetered one digit, it solved entire board and would not show the algorithm on the GUI
                new.append(self.selected)
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def draw(self):
        # Draw the grid lines
        gap = self.width/9
        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(self.window, (0,0,0), (0, i*gap),(self.width, i *gap), thick)
            pygame.draw.line(self.window, (0,0,0), (i*gap, 0), (i*gap, self.height), thick)

        # Cubes are being drawing
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(self.window)

    def select(self, row, col):
        # Reset everything
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)


    def clear(self):
        row, col = self.selected
        if (self.cubes[row][col].value == 0) or (self.selected in new):
            self.cubes[row][col].set_temp(0)
            self.cubes[row][col].set(0)

    def click(self, pos):
        """
        :param pos:
        :return: (row, col)
        """

        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width/9
            x = pos[0]//gap
            y = pos[1]//gap
            return (int(y), int(x))
        else:
            return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True

    def solve(self):
        print(self.model)
        find = find_empty(self.model)
        print(find)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1,10):
            if valid(self.model, i, (row, col)):
                self.model[row][col] = i

                if self.solve():
                    return True
                self.model[row][col] = 0
        return False

    def solve_GUI(self):
        find = find_empty(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1,10):
            if valid(self.model, i, (row, col)):
                self.model[row][col] = i
                self.cubes[row][col].set(i)
                self.cubes[row][col].draw_change(self.window, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(100)

                if self.solve_GUI():
                    return True

                self.model[row][col] = 0
                self.cubes[row][col].set(0)
                self.update_model()
                self.cubes[row][col].draw_change(self.window, False)
                pygame.display.update()
                pygame.time.delay(100)

        return False


class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, window):
        font = pygame.font.SysFont("Times New Roman", 30)
        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = font.render(str(self.temp),1, (128,128,128))
            window.blit(text, (x+5, y+5))
        elif self.temp != 0 and not(self.value == 0):
            text = font.render(str(self.value), 1, (0, 0, 255))  # newly placed numbers will be blue
            window.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))
        elif not(self.value == 0):
            text = font.render(str(self.value), 1, (0,0,0))
            window.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

        if self.selected:
            pygame.draw.rect(window, (255,0,0), (x,y,gap,gap), 3)

    def draw_change(self, window, g =True):
        font = pygame.font.SysFont("Times New Roman", 30)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap
        pygame.draw.rect(window, (255,255,255), (x,y,gap,gap), 0)

        text = font.render(str(self.value), 1, (0,0,255))
        window.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))
        if g:
            pygame.draw.rect(window,(0,255,0), (x,y,gap,gap), 2)
        else:
            pygame.draw.rect(window, (255,0,0), (x,y,gap,gap), 2)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val


def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                #return the row and col
                return (i,j)
    return None


def valid(bo, num, pos):
    # Check in the row
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    # Check in the column
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    # Check in the box
    box_x = pos[1]//3
    box_y = pos[0]//3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x*3, box_x*3 + 3):
            if bo[i][j] == num and (i,j) != pos:
                return False

    return True

def redraw_window(window, board, time, strikes):
    window.fill((255,255,255))
    # Drawing the time
    font = pygame.font.SysFont("Times New Roman", 30)
    text = font.render("Time "+ format_time(time),1, (0,0,0))
    window.blit(text, (540 - 180, 560))
    # Drawing Wrong answers/Strikes
    text = font.render("X "* strikes,1,(255,0,0))
    window.blit(text, (20, 560))
    # Draw the grid and board
    board.draw()


def format_time(secs):
    seconds = secs%60
    minutes = secs//60
    hours = minutes//60
    return " " + str(minutes) + ":" + str(seconds)


def main():
    window = pygame.display.set_mode((540,600))
    pygame.display.set_caption("Sudoku")
    board = Grid(9,9,540,540,window)
    key = None
    run = True
    start = time.time()
    strikes = 0
    while run:
        if not board.is_finished():
            active_time = round(time.time() - start)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    board.solve_GUI()
                elif (event.key == pygame.K_1) or (event.key == pygame.K_KP1):
                    key = 1
                elif (event.key == pygame.K_2) or (event.key == pygame.K_KP2):
                    key = 2
                elif (event.key == pygame.K_3) or (event.key == pygame.K_KP3):
                    key = 3
                elif (event.key == pygame.K_4) or (event.key == pygame.K_KP4):
                    key = 4
                elif (event.key == pygame.K_5) or (event.key == pygame.K_KP5):
                    key = 5
                elif (event.key == pygame.K_6) or (event.key == pygame.K_KP6):
                    key = 6
                elif (event.key == pygame.K_7) or (event.key == pygame.K_KP7):
                    key = 7
                elif (event.key == pygame.K_8) or (event.key == pygame.K_KP8):
                    key = 8
                elif (event.key == pygame.K_9) or (event.key == pygame.K_KP9):
                    key = 9
                elif (event.key == pygame.K_DELETE) or (event.key == pygame.K_BACKSPACE):
                    board.clear()
                    key = None
                elif (event.key == pygame.K_RETURN) or (event.key == pygame.K_KP_ENTER):
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if board.place(board.cubes[i][j].temp):
                            print("Successful Placement!")
                        else:
                            print("Wrong Placement!")
                            strikes += 1
                        key = None

                if board.is_finished():
                    # make popup appear to give congratulations
                    print("Game is over. Board solved: Congratulations")

            if (event.type == pygame.MOUSEBUTTONDOWN) or (event.type == pygame.MOUSEBUTTONUP):
                pos = pygame.mouse.get_pos()
                click = board.click(pos)
                if click:
                    board.select(click[0], click[1])
                    key = None
            if strikes == 3:
                print("Game is over. You got 3 strikes.")
                run = False

        if board.selected and key != None:
            board.sketch(key)

        redraw_window(window, board, active_time, strikes)
        pygame.display.update()



main()
pygame.quit()
sys.exit