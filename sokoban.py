import board
import player
import goal

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

while True:
    print("Make a move:", end=" ")
    move = input()
    if move == "q":
        break
    if move == "r":
        board.start()
    if move == "info":
        info()
    else:
        player.move(move)
    
    board.printB()

    if goal.is_winner():
        print("YOU WIN!")
        break

