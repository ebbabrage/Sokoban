import player
import goal
import portal
board = []
hint = ()

# Symbol dictionary for terminal game
symbols = {
    "w" : "#",
    "o" : " ",
    "b" : "\u25A0",
    "g" : "\u2606",
    "p" : "\u25CB",
    "t" : "|",
    "h" : "\u25A1"
}

def start(lvl):
    '''  Set initial gameboard  '''
    global board 
    goal.reset()
    portal.reset()
    match lvl:
        case "1":
            board = [
                    ["w", "w", "w", "w", "w", "w"],
                    ["w", "p", "o", "b", "g", "w"],
                    ["w", "o", "b", "w", "w", "w"],
                    ["w", "o", "o", "o", "g", "w"],
                    ["w", "w", "w", "w", "w", "w"]
                    ]
            # Initial positions
            player.uppdate_pos(1,1)
            goal.add(1,4)
            goal.add(3,4)
        case "2":
            board = [
                    ["w", "w", "w", "w", "w", "w", "w"],
                    ["w", "o", "t", "o", "g", "w", "w"],
                    ["w", "o", "w", "w", "w", "w", "w"],
                    ["w", "p", "o", "b", "o", "t", "w"],
                    ["w", "o", "w", "b", "w", "w", "w"],
                    ["w", "o", "o", "o", "o", "g", "w"],
                    ["w", "w", "w", "w", "w", "w", "w"]
                    ]
            # Initial positions
            player.uppdate_pos(3,1)
            goal.add(1,4)
            goal.add(5,5)
            portal.add(3,5)
            portal.add(1,2)

def printB():
    '''  Print curent board   '''
    global board
    for r in range(len(board)):
        for c in range(len(board[r])):
            print(symbols[board[r][c]], end=" ")
        print()

def get_board():
    ''' Returns the board '''
    global board
    return board

def show_hint(hints):
    ''' Adds hint to board '''
    global board, hint
    oldPos = player.get_pos()

    for h in hints:
        row = int(h[0])
        col = int(h[1])
        
        if board[row][col] == "b":
            # Get position for hint
            if row - oldPos[0] != 0:
                d = row - oldPos[0]
                board[row + d][col] = "h"
                hint = (row + d, col)
            else:
                d = col - oldPos[1]
                board[row][col + d] = "h"
                hint = (row, col + d)
            return True
        oldPos = (row, col)

def was_hint(r,c):
    global hint
    if hint == (r,c):
        return True

def uppdate(oldPos, newPos, toMove):
    '''  Uppdate the board  '''
    global board, hint

    if toMove == "b" and board[newPos[0]][newPos[1]] == "h": # Hint
        if goal.was_goal(newPos[0], newPos[1], "h"):
            board[newPos[0]][newPos[1]] = "g"
        elif portal.was_portal(newPos[0], newPos[1], "h"):
            board[newPos[0]][newPos[1]] = "t"
        else:
            board[newPos[0]][newPos[1]] = "o"  
        hint = ()
    
    match board[newPos[0]][newPos[1]]:
        case "w": # Wall
            return False
        
        case "o": # Open space
            board[newPos[0]][newPos[1]] = toMove
        
        case "g": # Goal
            if toMove == "b":
                goal.box_in_goal()
            
            board[newPos[0]][newPos[1]] = toMove
        
        case "b": # Box
            if toMove != "b":
                boxMove = ()

                # Get new position for box
                if newPos[0] - oldPos[0] != 0:
                    d = newPos[0] - oldPos[0]
                    boxMove = (newPos[0] + d, newPos[1])
                else:
                    d = newPos[1] - oldPos[1]
                    boxMove = (newPos[0], newPos[1] + d)

                # Move box if possible
                if uppdate((newPos[0], newPos[1]), boxMove, "b"):
                    board[newPos[0]][newPos[1]] = toMove
                else:
                    return False
            else:
                return False
        
        case "t": # Portal
            if toMove == "b":
                newPos = portal.box_in_portal(newPos[0],newPos[1])
                # If box already on portal
                if board[newPos[0]][newPos[1]] == "b":
                    return False
            
            board[newPos[0]][newPos[1]] = toMove

        case "h": # Hint
            board[newPos[0]][newPos[1]] = toMove

    # What was the original space
    og = ""
    if goal.was_goal(oldPos[0], oldPos[1], toMove):
        og = "g"
    elif portal.was_portal(oldPos[0], oldPos[1], toMove):
        og = "t"
    elif was_hint(oldPos[0], oldPos[1]):
        og = "h"
    else:
        og = "o"  

    board[oldPos[0]][oldPos[1]] = og
    return True