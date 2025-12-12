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

info()
board.start()
board.printB()

def get_hint(hint):
    # get the board
    board_state = board.get_board()

    # make list to put rows in
    rows = []

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
                rows.append(f"box({row},{col}).")

            if pos == "g":
                rows.append(f"goal({row},{col}).")

            if pos == "p":    
                rows.append(f"player_pos({row},{col}).")

    #write the lp file
    with open(hint, "w") as f:
        f.write("\n".join(rows))
    
    # run new lp file with lp-solver
    result = subprocess.run(["clingo", "hint.lp", "sokoban_solver.lp"],
        output = True,
        text = True
    )
    
    sokoban_solver_output = result.stdout

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
        get_hint()
    else:
        player.move(move)
    
    board.printB()

    if goal.is_winner():
        print("YOU WIN!")
        break
