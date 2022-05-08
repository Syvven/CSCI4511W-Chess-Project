import board
import sys, time

base_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
time_test_fen = "r1b1k1nr/p2p1pNp/n2B4/1p1NP2P/6P1/3P1Q2/P1P1K3/q5b1"

def new_game(mode, ver, restart=False):
    # sets up the turtle screen 
    # tracer set to 0 so that that pesky turtle is kept out of sight
    # done in case of restart
    if not restart:
        board.sc.setup(width=1200, height=1000)
        board.sc.tracer(0,0)
        board.tr.speed('fastest')
        board.tr.ht()
        # undo buffer in order to undo things if needed
        board.tr.setundobuffer(10000)
        board.turn_tr.hideturtle()
        board.turn_tr.setundobuffer(1000)

    # board is where most of the functions take place
    b = board.Board(mode, ver)
    # the board is drawn at the beginning based off the global starting fen string
    b.draw_board()
    b.load_from_fen(base_fen)
    # # b.load_from_fen(time_test_fen)
    b.update_pieces()
    
    b.draw_promos()

    b.switch_turn_turtle()

    # time testing code

    # t1 = time.perf_counter()
    # t3 = 0
    # t4 = 0
    # t5 = 0
    # t6 = 0
    # for i in range(1000):
    #     t5 += time.perf_counter()
    #     all_moves = b.generate_all_moves()
    #     t6 += time.perf_counter()
    #     t3 += time.perf_counter()
    #     b.check_for_check(all_moves)
    #     t4 += time.perf_counter()
    # t2 = time.perf_counter()
    # print("total time:", t2-t1)
    # print("mean total time:", (t2-t1)/100, "\n")
    # print("mean generate time:", (t6-t5)/100)
    # print("total generate time:", t6-t5, "\n")
    # print("mean check time:", (t4-t3)/100)
    # print("total check time:", t4-t3, "\n")
    # return

    # b.all_moves = b.generate_all_moves()
    # b.check_for_check(b.all_moves)
    # b.get_move_from_search(b.all_moves, 1)
    # print(b.leaves_reached)
    # return

    # listen for any key/button events
    # "r" restarts the game, bringing the board back to the beginning
    # "t" closes the screen and shuts down the program nicely
    # mb1 starts the main loop of the game
    board.sc.listen()
    board.sc.onkeypress(b.restart_game, "r")
    board.sc.onkeypress(b.game_over, "q")
    board.sc.onclick(b.start_square)
    b.time_start = time.perf_counter()
    board.sc.mainloop()

def main():
    # gets the input command line arguments
    argv = sys.argv[1:]
    argc = len(argv)

    # if there are no command line arguments
    if not argv:
        print("Usage: python3 chess-new.py <mode> <ai-version>\n")
        return 

    # extract the mode -- should be "ai" or "two-player"
    mode = argv[0].lower()
    
    # if the second argument is not a number, error
    try:
        ai_ver = int(argv[1])
    except:
        print("Usage: python3 chess-new.py <mode> <ai-version>\n")
        return

    # make sure that the arguments are formatted correctly
    err = False
    if mode != 'two-player' and mode != 'ai':
        err = True
    if mode == 'two-player' and ai_ver != 0:
        err = True
    if mode == 'ai' and not (1 <= ai_ver <= 3):
        err = True
    if err:
        print("Usage: python3 chess-new.py <mode> <ai-version>\n")
        return

    new_game(mode, ai_ver)

if __name__ == '__main__':
    main()