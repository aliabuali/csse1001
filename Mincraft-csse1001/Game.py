"""
CSSE1001 2019s2a1
Name: Ali Abu Ali
Student Number:45609196
"""
from a1_support import *
score = 0
# Write the expected functions here
def get_position_in_direction(position, direction):
    """Returns the positon (x,y) that would will change the
     given position in the given direction.

    Parameters:
        position(tuple): the position of the player.
        direction(str): the direction where the player wants to move.

    Returns:
        (tuple<int, int>): the row, column positon of a tile.
    """
    new_position = DIRECTIONS[direction] # the new (x,y) coordinate <tuple>
    position = list(position)
    new_position = list(new_position)
    #Modifying the current position
    position[0]+=new_position[0]
    position[1]+=new_position[1]
    position = tuple(position)
    new_position = (0,0)
    return position

def get_tile_at_position(level, position):
    """ Return the symbol that represents the tile
     at the given position in a level string.

    Parameters:
        level(str): the level string.
        position(tuple<int, int>): the row, column positon of a tile.

    Return:
        (str): the character at the given position.
    """

    size = level_size(level) # returns the dimension (x,y) level size
    tile_index = position_to_index(position, size) # the index of the tile
    return level[tile_index]

def get_tile_in_direction(level, position, direction):
    """ Determaine the tile after moving the position in the given direction,
     and return the character in the upadated position.

    Parameters:
        level(str): the level string.
        position(tuple<int, int>): the row, column positon of a tile.
        direction(str): the direction where the player wants to move.

    Return:
        (str): the tile at the updated position.
    """
    updated_position = get_position_in_direction(position,direction)
    updated_tile = get_tile_at_position(level, updated_position)
    return updated_tile

def print_level(level, position):
    """Prints the level with the title of the given position
     replaced by the player tile.

    Parameters:
        level(str): the level string.
        position (tuple<int, int>): The row, column position of a tile.
    """
    size = level_size(level) # returns the dimension (x,y) level size
    player_index = position_to_index(position, size) # the index of the tile
    print(level[:player_index]+PLAYER+level[player_index+1:])

def remove_from_level(level, position):
    """ Returns a level string excluding the given position,
     replaced by air tile.

    Parameter:
        level(str): The level string.
        position (tuple<int, int>): The row, column position of a tile.

    Return:
        (str): The level string, after excluding the given position.
    """
    size = level_size(level) # returns the dimension (x,y) level size
    index = position_to_index(position, size) # the index of the tile
    return level[:index]+AIR+level[index+1:]

def move(level, position, direction):
    """ Return the updated position after moving the tile in the given
    direction.
    New position should be an air tile and below it should not be an air.

    Parameter:
        level(str): The level string.
        psoition(tuple<int, int>): The row, colunm position of a tile.
        direction(str): the direction where the tile will be moved.

    Return:
        (tuple<int, int>): The updated positon after moving in direction.
    """
    # The updated position
    new_position = get_position_in_direction(position, direction)
    new_tile = get_tile_at_position(level, new_position)
    # Testing if the updated position is a WALL,
    # move it up until an air is found:
    while new_tile == WALL   :
        new_position = get_position_in_direction(new_position, "u") # moving up
        new_tile = get_tile_at_position(level, new_position)
    # move down
    while get_tile_at_position(level,
    get_position_in_direction(new_position, "d")) == AIR:
        new_position = get_position_in_direction(new_position, "d")
    # while test the position value using another tuple:
    return new_position

def attack(level, position):
    """ Attack the monter after printing a warning message if there is a monter
     tile on the player's right or left and return
     the level with the monster removed. Else, return the level unchanged.

    Parameters:
        level(str): the level string.
        position(tuple<int,int>): the position of the tile.

    Return:
        (str): the level with the monster removed, or unchanged if there is no.
    """
    # Get tiles on both direction
    left_tile = get_tile_in_direction(level, position, "l")
    # Get positions in both directions
    left_position = get_position_in_direction(position, "l")
    right_tile = get_tile_in_direction(level, position, "r")
    right_position = get_position_in_direction(position, "r")
    # Check if the monster tile is on right or left of the player
    if right_tile!="@"!=left_tile:
        print("No monsters to attack!")
        return level
    if left_tile=="@":
            print("Attacking the monster on your left!")
            level = remove_from_level(level,left_position)
    elif right_tile=="@":
            print("Attacking the monster on your right!")
            level = remove_from_level(level,right_position)
    return level

def tile_status(level, position):
    """ Return a tuple with tile and the level and printing a
     message indicating the tile status.

    Parameters:
        level(str): the level string.
        position(tuple<int,int>): the position of the tile.

    Return:
        (tuple<str,str>): tuple with the first value is the tile character
        , and the second is the level string.
    """
    tile = get_tile_at_position(level, position)
    if tile == GOAL:
        print("Congratulations! You finished the level")

    elif tile == MONSTER:
        print("Hit a monster!")

    elif tile== COIN or tile== CHECKPOINT:
        level = remove_from_level(level, position)
    return ((tile, level))

def main():
    """Handles the main intereaction with the user."""
    score = 0
    player = (0,1)
    # game_on = True
    level = input("Please enter the name of the level file (e.g. level1.txt): ")
    game = load_level(level)
    reset_position = 0
    while True :
        print("Score:",score)
        print_level(game, player)
        user = input("Please enter an action (enter '?' for help): ")
        if  user == "?":
            print(HELP_TEXT)
        elif user=="a":
            game = attack(game,player)
        elif user=="q":
            break
        elif user in "udrl":
            new_position = get_position_in_direction(player, user)
            status = tile_status(game, new_position)
            tile = status[0] #get the new tile
            game = status[1] # updating the level
            if tile == COIN  :
                score+=1
            elif tile == GOAL:
                break
            elif tile == CHECKPOINT:
                reset_position =  new_position
            elif tile == MONSTER :
                if reset_position!=0:
                    player = (reset_position[0]-1,reset_position[1])
                else:
                    break
            player = move(game, player, user )
        elif user=="n":
            player = reset_position

if __name__ == "__main__":
    main()
