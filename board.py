import player
import goal
import portal
board = []

symbols = {
    "w" : "#",
    "o" : " ",
    "b" : "\u25A0",
    "g" : "\u2606",
    "p" : "\u25CB",
    "t" : "|"
}

def start():
    '''  Set initial gameboard  '''
    global board 
    # board = [
    #         ["w", "w", "w", "w", "w"],
    #         ["w", "o", "g", "o", "w"],
    #         ["w", "o", "o", "o", "w"],
    #         ["w", "o", "b", "o", "w"],
    #         ["w", "o", "p", "o", "w"],
    #         ["w", "w", "w", "w", "w"]
    #         ]
    # player.uppdate_pos(4,2)
    # goal.add_goal(1,2)
    # board = [
    #         ["w", "w", "w", "w", "w", "w"],
    #         ["w", "p", "o", "b", "g", "w"],
    #         ["w", "o", "b", "w", "w", "w"],
    #         ["w", "o", "o", "o", "g", "w"],
    #         ["w", "w", "w", "w", "w", "w"]
    #         ]
    # player.uppdate_pos(1,1)
    # goal.add_goal(1,4)
    # goal.add_goal(3,4)
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
    goal.add_goal(1,4)
    goal.add_goal(5,5)
    portal.add_portal(3,5)
    portal.add_portal(1,2)

def printB():
    '''  Print curent board   '''
    global board
    for r in range(len(board)):
        for c in range(len(board[r])):
            print(symbols[board[r][c]], end=" ")
        print()

def uppdate(oldPos, newPos, toMove):
    '''  Uppdate the board  '''
    global board
    
    match board[newPos[0]][newPos[1]]:
        case "w": # Wall
            return False
        
        case "o": # Open space
            board[newPos[0]][newPos[1]] = toMove

            # What was the original space
            if goal.was_goal(oldPos[0], oldPos[1], toMove):
                board[oldPos[0]][oldPos[1]] = "g"
            elif portal.was_portal(oldPos[0], oldPos[1], toMove):
                board[oldPos[0]][oldPos[1]] = "t"
            else:
                board[oldPos[0]][oldPos[1]] = "o"  
            return True
        
        case "g": # Goal
            if toMove == "b":
                goal.box_in_goal()
            
            board[newPos[0]][newPos[1]] = toMove

            # What was the original space
            if goal.was_goal(oldPos[0], oldPos[1], toMove):
                board[oldPos[0]][oldPos[1]] = "g"
            elif portal.was_portal(oldPos[0], oldPos[1], toMove):
                board[oldPos[0]][oldPos[1]] = "t"
            else:
                board[oldPos[0]][oldPos[1]] = "o"
            return True
        
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

                    # What was the original space
                    if goal.was_goal(oldPos[0], oldPos[1], toMove):
                        board[oldPos[0]][oldPos[1]] = "g"
                    elif portal.was_portal(oldPos[0], oldPos[1], toMove):
                        board[oldPos[0]][oldPos[1]] = "t"
                    else:
                        board[oldPos[0]][oldPos[1]] = "o"
                    return True
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

            # What was the original space
            if goal.was_goal(oldPos[0], oldPos[1], toMove):
                board[oldPos[0]][oldPos[1]] = "g"
            elif portal.was_portal(oldPos[0], oldPos[1], toMove):
                board[oldPos[0]][oldPos[1]] = "t"
            else:
                board[oldPos[0]][oldPos[1]] = "o"
            return True

def get_board():
    global board
    return board