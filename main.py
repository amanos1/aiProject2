# Alright, what are we gonna need for this?
# We need a function (or several) to make the grid and randomly give the spaces different terrains
# There is a main function that does the following:
# Calls the function to generate the random grid
# Places the agent on a random square
# Has a loop that calls three functions:
# 1, Generates a random direction
# 2, Moves the agent in that direction 90% of the time
# 3, Gives the reading of the current terrain, with 90% accuracy
# After it has done this 100 times, it will store in a text file the data it has which will be stored in 3 arrays

import random
from math import ceil

NORMAL = 'N'
HIGHWAY = 'H'
HARD_TO_TRAVERSE = 'T'
BLOCKED = 'B'

UP = 'U'
DOWN = 'D'
LEFT = 'L'
RIGHT = 'R'

graph = []
rows = 50
columns = 100

init_cell = ()
locations = []
directions = []
observations = []


class Cell:
    def __init__(self, x, y, state):
        self.x = x
        self.y = y
        self.state = state

    def get_state(self):
        return self.state


class Agent:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move_up(self):
        if self.y > 0:
            self.y -= 1

    def move_down(self):
        if self.y < rows - 1:
            self.y += 1

    def move_left(self):
        if self.x > 0:
            self.x -= 1

    def move_right(self):
        if self.x < columns - 1:
            self.x += 1

    def sniff(self):
        random_number = random.randrange(0, 100)
        smell = index(self.x, self.y).get_state()
        if random_number < 90:
            return smell
        options = [NORMAL, HIGHWAY, HARD_TO_TRAVERSE]
        options.remove(smell)
        return options[random_number % 2]

    def get_local(self):
        return self.x, self.y


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def generate_random_state():
    random_number = random.randrange(0, 100)
    if random_number < 50:
        return NORMAL
    elif random_number < 70:
        return HIGHWAY
    elif random_number < 90:
        return HARD_TO_TRAVERSE
    else:
        return BLOCKED


def populate_graph():
    total_cells = columns * rows
    normal = ceil(total_cells * 0.5)
    highway = total_cells * 0.2
    hard_to_traverse = total_cells * 0.2
    blocked = total_cells - normal - highway - hard_to_traverse
    for i in range(columns):
        for j in range(rows):
            state = 0
            while True:
                state = generate_random_state()
                random_number = random.randrange(0, 100)
                if random_number < 50:
                    state = NORMAL
                    if normal > 0:
                        normal -= 1
                        break
                elif random_number < 70:
                    state = HIGHWAY
                    if highway > 0:
                        highway -= 1
                        break
                elif random_number < 90:
                    state = HARD_TO_TRAVERSE
                    if hard_to_traverse > 0:
                        hard_to_traverse -= 1
                        break
                else:
                    state = BLOCKED
                    if blocked > 0:
                        blocked -= 1
                        break
            print(state, " ", end="")
            new_cell = Cell(i, j, state)
            graph.append(new_cell)
        print()


def traverse_graph():
    for i in range(50):
        random_number = random.randrange(0, 4)
        if random_number == 0:
            myAgent.move_up()
            directions.append(UP)
        elif random_number == 1:
            myAgent.move_down()
            directions.append(DOWN)
        elif random_number == 2:
            myAgent.move_left()
            directions.append(LEFT)
        else:
            myAgent.move_right()
            directions.append(RIGHT)


def write_to_file():
    return True


def index(x, y):
    return graph[(columns+1) * (y-1) + (x-1)]


if __name__ == '__main__':
    print_hi('PyCharm')
    global myAgent
    init_x = random.randrange(0, columns)
    init_y = random.randrange(0, rows)
    init_cell = (init_x, init_y)
    myAgent = Agent(init_x, init_y)
    populate_graph()
    # traverse_graph()
    # write_to_file()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
