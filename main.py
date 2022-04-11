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

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
