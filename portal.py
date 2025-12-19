portals = []

def reset():
    global portals
    portals = []

def add(r,c):
    '''  Add portal to list'''
    global portals
    portals.append((r,c))

def was_portal(r,c,toMove):
    '''  Returns true if square was a portal  '''
    global portals, finishedBoxes
    for portal in portals:
        if portal == (r,c):
            return True
        
def box_in_portal(r,c):
    '''  Return cordinates for teleportation  '''
    global portals, finishedBoxes
    for portal in portals:
        if portal != (r,c):
            return portal
    