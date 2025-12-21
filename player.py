import board
pos = (0, 0)

def uppdate_pos(r, c):
    '''  Uppdate cordinates for players position  '''
    global pos
    pos = (r, c)

def move(move):
    '''  Move player in board  '''
    global pos
    match move:
        case "w": # Up
            newPos = (pos[0] - 1, pos[1])
        case "a": # Left
            newPos = (pos[0], pos[1] - 1)
        case "s": # Down
            newPos = (pos[0] + 1, pos[1])
        case "d": # Right
            newPos = (pos[0], pos[1] + 1)
        case _: # Unknown
            print("Not a move")
            return 
    
    if board.uppdate(pos, newPos, "p"):
        pos = newPos
        return True
    else:
        print("Ivalid move")
        return False

def get_pos():
    ''' Returns position of player '''
    global pos
    return pos