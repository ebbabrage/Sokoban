import board
import player
import goal
import subprocess

def info():
    print("------------------------------")
    print("Here are the controls:")
    print("w - Up\na - Left\ns - Down\nd - Right\n")
    print("Other controls:")
    print("q - Quit\nr - Restart level\nhint - Get a hint\ninfo - Get this information again")
    print("------------------------------")

def sort_after(x):
    return x[2]

def get_hint():

    # get the board
    board_state = board.get_board()

    # list to put rows in
    rows = []
    goals = []
    portals = []

    for row in range(len(board_state)):
        for col in range(len(board_state[row])):
            pos = board_state[row][col]

            # either a wall or open
            if pos == "w":
                rows.append(f"cell({row},{col},wall).")
            else:
                rows.append(f"cell({row},{col},open).")

            # a box, goal or player position
            if pos == "b":
                rows.append(f"crate({row},{col}).")

            if pos == "g":
                goals.append((row,col))

            if pos == "p":    
                rows.append(f"player_position({row},{col}).")

            if pos == "t":
                portals.append((row,col))

    if len(portals) == 2:
        (fromRow,fromCol), (toRow,toCol) = portals

        rows.append(f"crate_one_way_teleporter({fromRow},{fromCol},{toRow},{toCol}).")
        rows.append(f"crate_one_way_teleporter({toRow},{toCol},{fromRow},{fromCol}).")

    # fixing formatting for goal_requirement
    goals_string = "goal_requirement :-"
    for x in goals:
        goals_string = goals_string + f"crate({x[0]},{x[1]},T),"

    goals_string = goals_string[:-1] + "."
    rows.append(goals_string)

    # write the lp file
    with open("hint.lp", "w") as f:
        f.write("\n".join(rows))
    
    # run new lp file with lp-solver
    result = subprocess.run(["clingo", "hint.lp", "sokoban_solver.lp"],
        capture_output = True,
        text = True
    )
    
    sokoban_solver_output = result.stdout
    split_result = sokoban_solver_output.split("\n")
    index = 0
    
    while (index < len(split_result)) and (split_result[index] != "OPTIMUM FOUND") : 
        index += 1
    
    if index == len(split_result):
        print("Board is not solvable, please reset to start over")
        return None

    split_result_list = split_result[index-2].split(" ")
    tripplet_list = []
    
    for x in split_result_list:
        tripplet_list.append(x[8:-1].split(","))

    tripplet_list.sort(key=sort_after)

    return tripplet_list

info()
while True:
    lvl = input("Choose a level (1-2): ")
    if int(lvl) > 0 and int(lvl) <= 2:
        board.start(lvl)
        board.printB()
        break
    print("Not a level")

while True:
    print("Make a move:", end=" ")
    move = input()
    if move == "q":
        break
    if move == "r":
        board.start()
    if move == "info":
        info()
    if move == "hint":
        hint = get_hint()
        board.show_hint(hint)
    else:
        player.move(move)
    board.printB()

    if goal.is_winner():
        print("YOU WIN!")
        break
