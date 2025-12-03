import board
import player
import goal

board.start()
board.printB()

while True:
    print("Make a move:", end=" ")
    move = input()
    if move == "q":
        break
    if move == "r":
        board.start()
    else:
        player.move(move)
    
    board.printB()

    if goal.is_winner():
        print("YOU WIN!")
        break