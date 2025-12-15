goals = []
finishedBoxes = 0

def add_goal(r,c):
    '''  Add goal to list'''
    global goals
    goals.append((r,c))

def was_goal(r,c,toMove):
    '''  Returns true if square was a goal  '''
    global goals, finishedBoxes
    for goal in goals:
        if goal == (r,c):
            if toMove == "b":
                finishedBoxes -= 1
            return True
        
def box_in_goal():
    '''  A box is in a goal  '''
    global finishedBoxes
    finishedBoxes += 1
    
def is_winner():
    '''  Returns true if all boxes are in goals'''
    global goals, finishedBoxes
    if len(goals) == finishedBoxes:
        return True
    else:
        return False
    