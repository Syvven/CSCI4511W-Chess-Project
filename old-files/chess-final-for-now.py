import turtle, math, copy, time, random

base_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
time_test_fen = "r1b1k1nr/p2p1pNp/n2B4/1p1NP2P/6P1/3P1Q2/P1P1K3/q5b1"

lauren = True
if lauren:
    B_BISHOP = "lauren-pieces/bbishop.gif"
    W_BISHOP = "lauren-pieces/wbishop.gif"
    B_KING = "lauren-pieces/bking.gif"
    W_KING = "lauren-pieces/wking.gif"
    B_KNIGHT = "lauren-pieces/bhorse.gif"
    W_KNIGHT = "lauren-pieces/whorse.gif"
    B_PAWN = "lauren-pieces/bpawn.gif"
    W_PAWN = "lauren-pieces/wpawn.gif"
    B_QUEEN = "lauren-pieces/bqueen.gif"
    W_QUEEN = "lauren-pieces/wqueen.gif"
    B_ROOK = "lauren-pieces/brook.gif"
    W_ROOK = "lauren-pieces/wrook.gif"
else:
    B_BISHOP = "pieces/bbishop.gif"
    W_BISHOP = "pieces/wbishop.gif"
    B_KING = "pieces/bking.gif"
    W_KING = "pieces/wking.gif"
    B_KNIGHT = "pieces/bhorse.gif"
    W_KNIGHT = "pieces/whorse.gif"
    B_PAWN = "pieces/bpawn.gif"
    W_PAWN = "pieces/wpawn.gif"
    B_QUEEN = "pieces/bqueen.gif"
    W_QUEEN = "pieces/wqueen.gif"
    B_ROOK = "pieces/brook.gif"
    W_ROOK = "pieces/wrook.gif"

tr = turtle.Turtle()
sc = tr.getscreen()
turn_tr = turtle.Turtle()


#####################################################
#               PIECE CLASS
#Easy API for getting values for piece type and color
#####################################################
class Piece:
    Nothing = 0
    King = 1
    Pawn = 2
    Knight = 3
    Bishop = 4
    Rook = 5
    Queen = 6
    White = 8
    Black = 16
    color_relation = {
        White: [-1, True, Black, 1],
        Black: [1, False, White, -1]
    }
    values = {
        Nothing: 0,
        White|King:     -90000,
        Black|King:      90000,
        White|Pawn:     -100,
        Black|Pawn:     100,
        White|Knight:   -300,
        Black|Knight:   300,
        White|Bishop:   -300,
        Black|Bishop:   300,
        White|Rook:     -500,
        Black|Rook:     500,
        White|Queen:    -900,
        Black|Queen:    900
    }

turn_tr_pos = {
    Piece.White: [425, -385,["White Turn!", True, "left", ('Arial', 20, 'italic', 'underline')]],
    Piece.Black: [425, 365,["Black Turn!", True, "left", ('Arial', 20, 'italic', 'underline')]]
}

#####################################################
#               SQUARE CLASS
#    Useful class for storing info about squares
#####################################################
class Square:
    def __init__(self, upleft, botright, piece):
        self.upleft = upleft
        self.botright = botright
        self.piece = piece 
        self.color = Piece.Nothing
        self.p_c = 0
        self.valid_moves = []
        self.index = None
        self.stamp_id = None
        self.castle = False
        self.doing_castle = False
        # self.en_passant = False
        # self.en_passanting = False
        self.white_c = False

    def __str__(self):
        return "({}, {}, {}, {}, {}, {})".format(self.index, self.p_c, self.piece, self.color, self.castle, self.doing_castle)
        

class AIPlayer:
    def __init__(self):
        # self.values = {
        #     Piece.King|Piece.Black: math.inf,
        #     Piece.King|Piece.White: -math.inf,
        #     Piece.Queen|Piece.Black: B_QUEEN,
        #     Piece.Queen|Piece.White: W_QUEEN,
        #     Piece.Bishop|Piece.Black: B_BISHOP,
        #     Piece.Bishop|Piece.White: W_BISHOP,
        #     Piece.Knight|Piece.Black: B_KNIGHT,
        #     Piece.Knight|Piece.White: W_KNIGHT,
        #     Piece.Rook|Piece.Black: B_ROOK,
        #     Piece.Rook|Piece.White: ,
        #     Piece.Pawn|Piece.Black: -100,
        #     Piece.Pawn|Piece.White: 100,
        # } 
        self.hi = 1

#####################################################
#               BOARD CLASS
#   The class in which most work will be done
#####################################################
class Board:
    # constructor
    def __init__(self):
        self.startx = -400
        self.starty = 400
        self.board = []
        self.old_board = []
        self.squares = []
        for i in range(64):
            self.board.append(0)
            self.old_board.append(0)
            self.squares.append(Square([0, 0], [0, 0], 0))
        self.selected_square = None
        self.white_turn = None
        self.swap_turn = False
        self.first_update = True
        self.valid_moves = []
        self.ai = AIPlayer()
        self.stamp_ids = []
        self.can_promote = False
        self.promote_s = None
        self.promoting = [False, 0]
        # self.pawndoubles = None
        # self.en_passanting = False
        self.all_moves = []
        self.turn_color = Piece.White
        self.white_king_ind = 0
        self.black_king_ind = 0
        self.just_castled = False
        self.just_promoted = False

        self.castled_info = []
        self.last_moves = []
        self.reset = False

        self.ai_turn = False
        self.total_available_moves = 0

        self.white_moves = 0
        self.black_moves = 0
        self.white_captured = 0
        self.black_captured = 0
        self.time_start = 0
        self.time_end = 0

        self.best_promote_piece = Piece.Queen

        self.move_path = []
        self.leaves_reached = 0

        self.fen_map = {
            'k': Piece.King,
            'p': Piece.Pawn, 
            'n': Piece.Knight,
            'b': Piece.Bishop, 
            'r': Piece.Rook,
            'q': Piece.Queen
        }

        self.piece_map = {
            Piece.King|Piece.Black:     B_KING,
            Piece.King|Piece.White:     W_KING,
            Piece.Queen|Piece.Black:    B_QUEEN,
            Piece.Queen|Piece.White:    W_QUEEN,
            Piece.Bishop|Piece.Black:   B_BISHOP,
            Piece.Bishop|Piece.White:   W_BISHOP,
            Piece.Knight|Piece.Black:   B_KNIGHT,
            Piece.Knight|Piece.White:   W_KNIGHT,
            Piece.Rook|Piece.Black:     B_ROOK,
            Piece.Rook|Piece.White:     W_ROOK,
            Piece.Pawn|Piece.Black:     B_PAWN,
            Piece.Pawn|Piece.White:     W_PAWN,
        }

        self.promo_map = {
            Piece.Queen:    [0,0,W_QUEEN],
            Piece.Bishop:   [0,0,W_BISHOP],
            Piece.Knight:   [0,0,W_KNIGHT],
            Piece.Rook:     [0,0,W_ROOK]
        }

        for key in self.piece_map:
            sc.register_shape(self.piece_map[key])

    # draws the initial board
    def draw_board(self):
        white = False;
        for rank in range(8):
            for file in range(8):
                tr.penup()
                x = self.startx+(file*100)
                y = self.starty-(rank*100)
                tr.setpos(x, y)
                tr.pendown()
                white = not white
                if white:
                    tr.fillcolor("#f5edb8")
                else:
                    tr.fillcolor('#b3202a')
                tr.begin_fill()
                for i in range(4):
                    tr.forward(100)
                    tr.right(90)
                tr.end_fill()
                square = self.squares[rank*8+file]
                square.white_c = not white
                square.upleft = [x, y]
                square.botright = [x+100, y-100]
                square.index = (rank*8+file)
            white = not white 
        sc.update()

    # loads a board state from a fen string
    def load_from_fen(self, fen):
        board_fen = fen.split()[0]
        file = 0
        rank = 0
        for ch in board_fen:
            if ch == '/':
                file = 0
                rank += 1
            else:
                if (ch.isdigit()):
                    file += (ord(ch) - ord('0'))
                else:
                    color = (Piece.White if ch.isupper() else Piece.Black)
                    ptype = self.fen_map[ch.lower()]
                    square = self.squares[rank*8+file]
                    self.board[rank*8+file] = ptype | color
                    self.old_board[rank*8+file] = ptype|color

                    square.piece = ptype
                    square.color = color
                    square.p_c = ptype|color

                    if ptype == Piece.King or ptype == Piece.Rook:
                        square.castle = True
                        if color == Piece.Black:
                            self.black_king_ind = rank*8+file
                        else:
                            self.white_king_ind = rank*8+file

                    file += 1
    
    # updates the board representation when needed
    # doesn't do redundant work
    def update_pieces(self):
        for rank in range(8):
            for file in range(8):
                curr_piece = self.board[rank*8+file]
                old_piece = self.old_board[rank*8+file]
                if self.first_update or old_piece != curr_piece:
                    self.old_board[rank*8+file] = curr_piece
                    if curr_piece != 0:
                        tr.shape(self.piece_map[curr_piece])
                        tr.penup()
                        tr.setpos(self.startx+(file*100)+50, self.starty-(rank*100)-50)
                        tr.pendown()
                        self.squares[rank*8+file].stamp_id = tr.stamp()
        sc.update()
        self.first_update = False

    def draw_promos(self):
        white = False
        tr.penup()
        x,y = self.startx-100,self.starty-50
        tr.goto(x, y+75)
        tr.write("Promotions", True, align="center", font=('Arial', 20, 'normal'))
        for key, value in self.promo_map.items():
            tr.goto(x,y)
            value[0], value[1] = x, y
            if white:
                tr.fillcolor("#f5edb8")
            else:
                tr.fillcolor('#b3202a')
            tr.shape('square')
            tr.pencolor('black')
            tr.shapesize(5, 5, 3)
            tr.stamp()
            tr.shape(value[2])
            tr.stamp()
            y -= 100
            white = not white
        sc.update()

    def promote_helper(self, x, y):
        if not self.ai_turn:
            print('inside promote_helper')
            valid = False
            sc.onkeypress(None, "z")
            for key,value in self.promo_map.items():
                if (value[0] <= x <= value[0]+100) and (value[1] >= y >= value[1]-100):
                    self.promote_s.piece = key
                    self.promote_s.p_c = key|self.promote_s.color
                    self.board[self.promote_s.index] = self.promote_s.p_c
                    tr.clearstamp(self.promote_s.stamp_id)
                    valid = True
                    self.update_pieces()
            if valid:
                sc.onclick(None)
                self.promoting[0] = False
                self.ai_turn = True
                # for random AI
                # self.AI_turn_random()

                # for AI using only heuristic
                self.AI_variable_depth()
        else:
            self.promote_s.piece = self.best_promote_piece
            self.promote_s.p_c = self.best_promote_piece | self.promote_s.color 
            self.board[self.promote_s.index] = self.promote_s.p_c 
            tr.clearstamp(self.promote_s.stamp_id)
            self.promoting[0] = False
            
            
    # promote a pawn when it reaches the enemy king row
    def promote(self, index):
        if not self.ai_turn:
            sc.onclick(None)
            sc.onclick(None, 3)
            print("promoting")
            for stamp in self.stamp_ids:
                tr.clearstamp(stamp)
            self.update_pieces()
            self.promote_s = self.squares[index]
            sc.onclick(self.promote_helper)
            sc.mainloop()
        else:   
            self.promote_s = self.squares[index]
            self.promote_helper(0,0)
            
    # checks for the possibility of castling
    # updates valid moves if so
    def check_castle(self, src, moves):
        square = src
        index = square.index
        if square.castle:
            if self.squares[index+1].piece == Piece.Nothing and self.squares[index+2].piece == Piece.Nothing:
                if self.squares[index+3].piece == Piece.Rook and self.squares[index+3].castle:
                    moves.append(self.squares[index+2])
                    self.squares[index+2].doing_castle = True
            if ((self.squares[index-1].piece == Piece.Nothing) and (self.squares[index-2].piece == Piece.Nothing) and (self.squares[index-3].piece == Piece.Nothing)):
                if self.squares[index-4].piece == Piece.Rook and self.squares[index-4].castle:
                    moves.append(self.squares[index-2])
                    self.squares[index-2].doing_castle = True

    # finds the possible moves for a pawn
    # and adds them to valid moves
    def check_pawn(self, src, moves):
        square = src
        index = square.index

        i = -1
        if square.color == Piece.Black:
            i = 1

        if (0 <= index+8*i <= 63):
            consider_square = self.squares[index+8*i]
            if (consider_square.piece == Piece.Nothing):
                moves.append(consider_square)
                if ((48 <= index <= 55) or (8 <= index <= 15)) and (0 <= index+16*i <= 63):
                    consider_square = self.squares[index+16*i]
                    if consider_square.piece == Piece.Nothing:
                        moves.append(consider_square)
                        # self.squares[index+8*i].en_passant = True
                        # self.pawndouble = consider_square
        
        if ((index+7*i)//8) == ((index//8)+1*i) and (0 <= index+7*i <= 63):
            consider_square = self.squares[index+7*i]
            # if (consider_square.piece == Piece.Nothing):
            #     if consider_square.en_passant and self.en_passanting:
            #         moves.append(consider_square)
            #         consider_square.en_passanting = True
            # following should be elif when enpassant
            if (consider_square.color|square.color) != square.color:
                moves.append(consider_square)
            

        if ((index+9*i)//8) == ((index//8)+1*i) and (0 <= index+9*i <= 63):
            consider_square = self.squares[index+9*i]
            # if (consider_square.piece == Piece.Nothing):
            #     if consider_square.en_passant and self.en_passanting:
            #         moves.append(consider_square)
            #         consider_square.en_passanting = True
            # following should be elif when enpassant
            if (consider_square.color|square.color) != square.color:
                moves.append(consider_square)
            

    # finds the possible moves for a knight
    # and adds them to valid moves
    def check_knight(self, src, moves):
        square = src
        index = square.index

        if (index+17) < 64 and (index%8) != 7:
                move_square = self.squares[index+17]
                if move_square.piece == Piece.Nothing or (move_square.color|square.color != square.color):
                    moves.append(move_square)
        if (index+15) < 64 and (index%8) != 0:
                move_square = self.squares[index+15]
                if move_square.piece == Piece.Nothing or (move_square.color|square.color != square.color):
                    moves.append(move_square)
        if (index+6) < 64 and (index%8) > 1:
                move_square = self.squares[index+6]
                if move_square.piece == Piece.Nothing or (move_square.color|square.color != square.color):
                    moves.append(move_square)
        if (index+10) < 64 and (index%8) < 6:
                move_square = self.squares[index+10]
                if move_square.piece == Piece.Nothing or (move_square.color|square.color != square.color):
                    moves.append(move_square)
        if (index-15) >= 0 and (index%8) != 7:
                move_square = self.squares[index-15]
                if move_square.piece == Piece.Nothing or (move_square.color|square.color != square.color):
                    moves.append(move_square)
        if (index-17) >= 0 and (index%8) != 0:
                move_square = self.squares[index-17]
                if move_square.piece == Piece.Nothing or (move_square.color|square.color != square.color):
                    moves.append(move_square)
        if (index-6) >= 0 and (index%8) < 6:
                move_square = self.squares[index-6]
                if move_square.piece == Piece.Nothing or (move_square.color|square.color != square.color):
                    moves.append(move_square)
        if (index-10) >= 0 and (index%8) > 1:
                move_square = self.squares[index-10]
                if move_square.piece == Piece.Nothing or (move_square.color|square.color != square.color):
                    moves.append(move_square)

    # checks if dist number squares in both horizontal directions
    # can be moved to and adds them to valid moves if so
    def check_horizontal(self, dist, src, moves):
        square = src
        index = square.index
        for i in range(1, dist+1):
            if ((index+i) > 63) or (((index+i)%8) == 0):
                break
            consider_square = self.squares[index+i]
            if consider_square.piece == Piece.Nothing:
                moves.append(consider_square)
                continue
            if consider_square.color == square.color:
                break
            if consider_square.color|square.color != square.color:
                moves.append(consider_square)
                break

        for i in range(1, dist+1):
            if ((index-i) < 0) or (((index-i)%8) == 7):
                break
            consider_square = self.squares[index-i]
            if consider_square.piece == Piece.Nothing:
                moves.append(consider_square)
                continue
            if consider_square.color == square.color:
                break
            if consider_square.color|square.color != square.color:
                moves.append(consider_square)
                break

    # checks if dist number squares in both vertical directions
    # can be moved to and adds them to valid moves if so
    def check_vertical(self, dist, src, moves):
        square = src
        index = square.index
        for i in range(1, dist+1):
            if (index+i*8) > 63:
                break
            consider_square = self.squares[index+i*8]
            if consider_square.piece == Piece.Nothing:
                moves.append(consider_square)
                continue
            if consider_square.color == square.color:
                break
            if consider_square.color|square.color != square.color:
                moves.append(consider_square)
                break
        for i in range(1, dist+1):
            if (index-i*8) < 0:
                break
            consider_square = self.squares[index-i*8]
            if consider_square.piece == Piece.Nothing:
                moves.append(consider_square)
                continue
            if consider_square.color == square.color:
                break
            if consider_square.color|square.color != square.color:
                moves.append(consider_square)
                break

    # checks if dist number squares in all diagonals
    # can be moved to and adds them to valid moves if so
    def check_diagonals(self, dist, src, moves):
        square = src
        index = square.index


        for i in range(1, dist+1):
            if (index-i*7) < 0 or ((index-i*7)%8) == 0:
                break
            move = self.squares[index-i*7]
            if move.color == square.color:
                break
            if move.piece == Piece.Nothing:
                moves.append(move)
            if move.color|square.color != square.color:
                moves.append(move)
                break
        for i in range(1, dist+1):
            if (index-i*9) < 0 or ((index-i*9)%8) == 7:
                break
            move = self.squares[index-i*9]
            if move.color == square.color:
                break
            if move.piece == Piece.Nothing:
                moves.append(move)
            if move.color|square.color != square.color:
                moves.append(move)
                break
        for i in range(1, dist+1):
            if (index+i*7) > 63 or ((index+i*7)%8) == 7:
                break
            move = self.squares[index+i*7]
            if move.color == square.color:
                break
            if move.piece == Piece.Nothing:
                moves.append(move)
            if move.color|square.color != square.color:
                moves.append(move)
                break
        for i in range(1, dist+1):
            if (index+i*9) > 63 or ((index+i*9)%8) == 0:
                break
            move = self.squares[index+i*9]
            if move.color == square.color:
                break
            if move.piece == Piece.Nothing:
                moves.append(move)
            if move.color|square.color != square.color:
                moves.append(move)
                break

    # checks for instances of check or checkmate
    def check_for_check(self, color):
        test_board = copy.deepcopy(self)

        for square in self.squares:
            remove_moves = []
            if square.piece != Piece.Nothing and square.color == color:
                for move in square.valid_moves:
                    test_square = test_board.squares[square.index]
                    test_move = test_board.squares[move.index]
                    op_color = Piece.color_relation[color][2]

                    test_board.move_piece(test_square, test_move, True)
                    test_board.generate_all_moves(op_color)

                    checked = False
                    for square2 in test_board.squares:
                        if square2.color == op_color:
                            for move2 in square2.valid_moves:
                                if move2.piece == Piece.King and move2.color == square.color:
                                    remove_moves.append(move)
                                    checked = True
                                    break
                            if checked:
                                break
                    test_board.undo_move_piece(check=True)
                for move in remove_moves:
                    self.total_available_moves -= 1
                    square.valid_moves.remove(move)

    # generates moves to be used in the main loop
    def generate_valid_moves(self, src, moves):
        p = src.piece
        if p == Piece.King:
            self.check_diagonals(1, src, moves)
            self.check_horizontal(1, src, moves)
            self.check_vertical(1, src, moves)
            self.check_castle(src, moves)
        elif p == Piece.Queen:
            self.check_diagonals(8, src, moves)
            self.check_horizontal(8, src, moves)
            self.check_vertical(8, src, moves)
        elif p == Piece.Bishop:
            self.check_diagonals(8, src, moves)
        elif p == Piece.Knight:
            self.check_knight(src, moves)
        elif p == Piece.Rook:
            self.check_vertical(8, src, moves)
            self.check_horizontal(8, src, moves)
        elif p == Piece.Pawn:
            self.check_pawn(src, moves)
    
    def generate_all_moves(self, color):
        self.total_available_moves = 0
        for square in self.squares:
            if square.piece != Piece.Nothing and square.color == color:
                square.valid_moves = []
                self.generate_valid_moves(square, square.valid_moves)
                self.total_available_moves += len(square.valid_moves)

    # puts overlay on board for possible moves
    def display_possible_moves(self):
        tr.penup()
        for move in self.valid_moves:
            tr.shape('square')
            if not move.white_c:
                tr.color('#A6A17C')
            else:
                tr.color('#591015')
            tr.shapesize(5, 5, 1)
            tr.shapesize(outline=2)
            tr.pencolor('black')    
            tr.goto(move.upleft[0]+50, move.upleft[1]-50)
            self.stamp_ids.append(tr.stamp())
            if move.p_c in self.piece_map:
                tr.shape(self.piece_map[move.p_c])
                self.stamp_ids.append(tr.stamp())
        sc.update()

    # helper for doing work to move when castling
    def move_castle(self, src, dst, test=False):
        print("castle")
        if dst.index%8 == 6:
            rook_ind = dst.index+1
            rook_d_ind = dst.index-1
        else:
            rook_ind = dst.index-2
            rook_d_ind = dst.index+1

        rook = self.squares[rook_ind]
        rook_dst = self.squares[rook_d_ind]

        add_castle = {}

        add_castle["src index"] = rook.index
        add_castle["src piece"] = rook.piece
        add_castle["src color"] = rook.color
        add_castle["src castle"] = rook.castle

        add_castle["dst index"] = rook_dst.index
        add_castle["dst piece"] = rook_dst.piece
        add_castle["dst color"] = rook_dst.color
        add_castle["dst castle"] = rook_dst.castle

        self.castled_info.append(add_castle)

        rook_dst.piece = rook.piece
        rook_dst.color = rook.color 
        rook_dst.p_c = rook.p_c

        rook.castle = False

        rook.piece = Piece.Nothing
        rook.color = Piece.Nothing
        rook.p_c = Piece.Nothing

        self.board[rook_ind] = 0
        self.board[rook_d_ind] = rook_dst.p_c

        self.just_castled = True

        self.stamp_ids.append(rook.stamp_id)

    # def move_en_passant(self, src, dst):
    #     print("en passant")
    #     i = 1
    #     if src.color == Piece.Black:
    #         i = -1

    #     pawn_sq = self.squares[dst.index+8*i]
    #     self.board[dst.index+8*i] = 0
    #     pawn_sq.piece = Piece.Nothing
    #     pawn_sq.color = Piece.Nothing
    #     pawn_sq.p_c = Piece.Nothing
    #     tr.clearstamp(pawn_sq.stamp_id)

    def undo_move_piece(self, check=False):
        self.reset = True
        src_index = self.last_moves[-1]["src index"]
        src_piece = self.last_moves[-1]["src piece"]
        src_color = self.last_moves[-1]["src color"]
        src_castle = self.last_moves[-1]["src castle"]
        j_castled = self.last_moves[-1]["just castled"]
        self.just_castled = j_castled
        src_moves = self.last_moves[-1]["src valid moves"]
        


        dst_index = self.last_moves[-1]["dst index"]
        dst_piece = self.last_moves[-1]["dst piece"]
        dst_color = self.last_moves[-1]["dst color"]
        dst_castle = self.last_moves[-1]["dst castle"]

        if dst_piece != Piece.Nothing:
            if dst_color == Piece.Black:
                self.white_captured -= 1
            else:
                self.black_captured -= 1

        if src_color == Piece.White:
            self.white_moves -= 1
        else:
            self.black_moves -= 1

        src = self.squares[src_index]
        src.piece = src_piece
        src.color = src_color
        src.p_c = src_piece | src_color
        src.castle = src_castle

        src.valid_moves = []
        for move in src_moves:
            src.valid_moves.append(self.squares[move.index])

        dst = self.squares[dst_index]
        dst.piece = dst_piece
        dst.color = dst_color
        dst.p_c = dst_piece | dst_color
        dst.castle = dst_castle

        dst.doing_castle = self.last_moves[-1]["dst doing castle"]

        self.last_moves.pop()

        self.board[src_index] = src.p_c
        self.board[dst_index] = dst.p_c

        if self.just_castled:
            rook = self.squares[self.castled_info[-1]["src index"]]
            rook_dst = self.squares[self.castled_info[-1]["dst index"]]
            
            rook.index = self.castled_info[-1]["src index"]
            rook.piece = self.castled_info[-1]["src piece"]
            rook.color = self.castled_info[-1]["src color"]
            rook.castle = self.castled_info[-1]["src castle"]
            rook.p_c = rook.color | rook.piece

            rook_dst.index = self.castled_info[-1]["dst index"]
            rook_dst.piece = self.castled_info[-1]["dst piece"]
            rook_dst.color = self.castled_info[-1]["dst color"]
            rook_dst.castle = self.castled_info[-1]["dst castle"]

            self.castled_info.pop()

            rook_dst.p_c = rook_dst.color | rook_dst.piece

            self.board[rook_dst.index] = rook_dst.p_c
            self.board[rook.index] = rook.p_c
            self.just_castled = False
            if not check:
                tr.clearstamp(rook_dst.stamp_id)

        if not check:
            tr.clearstamp(dst.stamp_id)
            self.change_turn(False)
            self.update_pieces()
            sc.onclick(None)
            sc.onclick(self.start_square)


    # does the work to move a piece
    # updates board rep and values for the squares
    def move_piece(self, src, dst, test=False):
        if self.just_castled:
            self.just_castled = not self.just_castled

        if dst.doing_castle and src.piece == Piece.King:
            self.move_castle(src, dst, test)
            

        # if dst.en_passanting and src.piece == Piece.Pawn:
        #     self.move_en_passant(src, dst)

        app_move = {}

        app_move["src index"] = src.index
        app_move["src piece"] = src.piece
        app_move["src color"] = src.color
        app_move["src castle"] = src.castle
        app_move["src valid moves"] = src.valid_moves

        app_move["dst index"] = dst.index
        app_move["dst piece"] = dst.piece
        app_move["dst color"] = dst.color
        app_move["dst castle"] = dst.castle
        app_move["dst doing castle"] = dst.doing_castle

        app_move["just castled"] = self.just_castled

        self.last_moves.append(app_move)

        if dst.piece != Piece.Nothing:
            if dst.color == Piece.Black:
                self.white_captured += 1
            else:
                self.black_captured += 1
        
        if src.color == Piece.White:
            self.white_moves += 1
        else:
            self.black_moves += 1

        dst.piece = src.piece
        dst.color = src.color
        dst.p_c = dst.piece | dst.color

        src.piece = Piece.Nothing
        src.color = Piece.Nothing 
        src.p_c = Piece.Nothing
        src.valid_moves = []

        self.board[dst.index] = dst.p_c
        self.board[src.index] = 0

        self.stamp_ids.append(src.stamp_id)
        self.stamp_ids.append(dst.stamp_id)

        for square in self.squares:
            square.doing_castle = False

        # if not test:
        for i in range(8):
            if self.squares[i].piece == Piece.Pawn:
                self.just_promoted = True
                if not test:
                    self.promoting[0] = True
                    self.promoting[1] = i
                    self.promote(i)
            if self.squares[56+i].piece == Piece.Pawn:
                self.just_promoted = True
                if not test:
                    self.promoting[0] = True
                    self.promoting[1] = 56+i
                    self.promote(56+i)


    def reset_helper(self, x, y):
        print("resetting")
        for stamp in self.stamp_ids:
            tr.clearstamp(stamp)
        self.stamp_ids = []
        sc.onclick(None)
        sc.onclick(self.start_square)
        sc.onclick(None, 3)

    def switch_turn_turtle(self):
        turn_tr.undo()
        args = turn_tr_pos[self.turn_color]
        turn_tr.penup()
        turn_tr.goto(args[0],args[1])
        turn_tr.color('black')
        turn_tr.pendown()
        turn_tr.write(*args[2])

    def change_turn(self, gen=True):
        # if the turn needs to be swapped, it is done
        self.white_turn = not self.white_turn
        self.swap_turn = False

        # sets color variable to be more easily checked against in a general case
        if self.white_turn:
            self.turn_color = Piece.White
        else:
            self.turn_color = Piece.Black

        if gen:
            self.generate_all_moves(self.turn_color)
            self.check_for_check(self.turn_color)

            game_over = True
            for square in self.squares:
                if (square.color == self.turn_color) and square.valid_moves:
                    game_over = False
                    break
        
            if game_over:
                self.game_over()
        self.switch_turn_turtle()

    # does work for selecting the destination square after selecting a piece
    def destination_square(self, x, y):
        print("looking for ending square")
        start = self.selected_square
        valid = False
        index = start.index

        for dst in self.squares:
            if (dst.upleft[0] <= x <= dst.botright[0]) and (dst.upleft[1] >= y >= dst.botright[1]):
                if dst in self.valid_moves:
                    sc.onclick(None)
                    sc.onkeypress(None, "z")
                    # if self.en_passanting:
                    #     self.move_piece(start, dst)
                    #     self.en_passanting = False
                    # else:
                    #     if dst == self.pawndouble:
                    #         self.en_passanting = True
                    #         print("pawn double")
                    # following move_piece call should be indented when enpassant
                    self.move_piece(start, dst)

                    for stamp in self.stamp_ids:
                        tr.clearstamp(stamp)
                    self.update_pieces()
                    valid = True
                    sc.onkeypress(self.undo_move_piece, "z")
                    break

        if valid:
            self.stamp_ids = []
            sc.onclick(self.start_square)
            sc.onclick(None, 3)

            if not self.ai_turn:
                sc.onclick(None)
                sc.onkeypress(None, 'z')
                # for random AI
                # self.AI_turn_random()

                # for AI with only heuristic
                self.AI_variable_depth()
                sc.onclick(None)
                sc.onkeypress(self.undo_move_piece, 'z')
                sc.onclick(self.start_square)

    # does work for selecting the piece to move
    def start_square(self, x=10000, y=100000):
        print("looking for starting square")
        # boolean to check that a piece was selected properly
        valid = False
        if self.reset:
            self.generate_all_moves(self.turn_color);
            self.check_for_check(self.turn_color);
            self.reset = False

        # loops through the squares
        for square in self.squares:
            # checks that the coordinates passed in through the onclick are within the bounds of any square
            # and that the color of the clicked on square corresponds to the color of the current turn
            if (square.upleft[0] <= x <= square.botright[0]) and (square.upleft[1] >= y >= square.botright[1]) and square.color == self.turn_color:
                # prints which piece is selected
                print("selected {}".format(square.piece))
                # some nice things for castling
                # resets the valid_moves list
                self.selected_square = square

                self.valid_moves = square.valid_moves

                # generates the moves for the specified piece 
                # those moves are stored in the valid moves class attribute
                # self.generate_valid_moves(self.selected_square, self.valid_moves)
                # self.check_for_check()

                # if there is at least one move, move on to the next function, otherwise, 
                # wait for another click and restart process
                if self.valid_moves:
                    # displays on the board the possible moves found from the previous call
                    self.display_possible_moves()
                    valid = True
                break

        # if a move was found, redirect the next click to a different function
        # this next click will correspond to where the clicked piece should be sent
        if valid:
            sc.onclick(None)
            sc.onclick(self.destination_square)
            # onclick is in case you want to decide you want to move a different piece
            # rightclicking after this point will restart this function and 
            # will allow you to pick a new piece
            sc.onclick(self.reset_helper, 3)
            # for square in self.squares:
            #     print(square)

    # evaluates board for AI
    # only one move deep
    def evaluate_ai_moves(self):
        print("evaluating moves")
        test_board = copy.deepcopy(self)
        best_moves = []
        curr_best = -math.inf
        for square in self.squares:
            if square.color == Piece.Black:
                src = test_board.squares[square.index]
                for move in square.valid_moves:
                    dst = test_board.squares[move.index]
                    curr = 0

                    test_board.move_piece(src, dst)
                    test_board.generate_all_moves(Piece.White)
                    test_board.check_for_check(Piece.White)
                    
                    for piece in test_board.board:
                        curr += Piece.values[piece]
                    
                    curr -= (test_board.total_available_moves*10)

                    if test_board.total_available_moves == 0:
                        return [[square, move]]

                    if curr_best < curr:
                        best_moves.clear()
                        best_moves.append([square,move])
                        curr_best = curr
                    elif curr_best == curr:
                        best_moves.append([square,move])
                    test_board.undo_move_piece(True)
        return best_moves

    def evaluate_variable(self, depth, color, board=None, alpha=(-math.inf), beta=math.inf):
        if board == None:
            board = copy.deepcopy(self)
            first = True
        else: 
            first = False
        if depth == 0:
            self.leaves_reached += 1
            curr = 0
            for piece in board.board:
                curr += Piece.values[piece]
            
            curr += Piece.color_relation[color][0]*(board.total_available_moves*10)
            if self.move_path:
                return [curr, self.move_path[0][0], self.move_path[0][1]]
            # testing purposes
            else:
                return [curr, None, None]

        board.generate_all_moves(color)
        board.check_for_check(color)

        ab_break = False
        bestVal = [Piece.color_relation[color][3]*math.inf, None, None]
        for square in board.squares:
            if first:
                self.move_path.clear()
            if square.color == color:
                for i in range(0,len(square.valid_moves)):
                    move = square.valid_moves[i]
                    self.move_path.append([self.squares[square.index], self.squares[move.index]])
                    # if square.piece == Piece.Rook and square.color == Piece.White:
                    #     for other in board.squares:
                    #         print(other)
                    #     print("Piece {} Color {} Before Move at depth {}:\n".format(square.piece, color, depth), board.board)
                    #     print(square.valid_moves)
                    board.move_piece(square, move, True)
                    # if move.piece == Piece.Rook and move.color == Piece.White:
                    #     for square in board.squares:
                    #         print(square)
                    #     print("Piece {} Color {} After Move at depth {}:\n".format(square.piece, color, depth), board.board)
                    #     print(square.valid_moves)
                    op_color = Piece.color_relation[color][2]
                    if board.just_promoted:
                        board.just_promoted = False
                        for piece in board.promo_map.keys():
                            move.piece = piece
                            board.generate_all_moves(op_color)
                            board.check_for_check(op_color)
                            if board.total_available_moves == 0:
                                board.undo_move_piece(True)
                                return [Piece.color_relation[color][3]*math.inf, self.move_path[0][0], self.move_path[0][1]]
                            value = self.evaluate_variable(depth-1, op_color, board, alpha, beta)
                            board.undo_move_piece(True)
                            if color == Piece.Black:
                                if value[0] >= bestVal[0]:
                                    bestVal = value
                                alpha = max(alpha, bestVal[0])
                            else:
                                if value[0] <= bestVal[0]:
                                    bestVal = value
                                beta = min(beta, bestVal[0])
                            if beta <= alpha:
                                ab_break = True
                                break
                    else:
                        
                        if board.total_available_moves == 0:
                            board.undo_move_piece(True)
                            return [Piece.color_relation[color][3]*math.inf, self.move_path[0][0], self.move_path[0][1]]
                        value = self.evaluate_variable(depth-1, op_color, board, alpha, beta)
                        board.undo_move_piece(True)
                        # if square.piece == Piece.Rook and square.color == Piece.White:
                        #     print("After Undo:\n",board.board)
                        #     print(square.valid_moves)
                        if color == Piece.Black:
                            if value[0] >= bestVal[0]:
                                bestVal = value
                            alpha = max(alpha, bestVal[0])
                        else:
                            if value[0] <= bestVal[0]:
                                bestVal = value
                            beta = min(beta, bestVal[0])
                        if beta <= alpha:
                            ab_break = True
                            break
                    self.move_path.pop()
            if ab_break:
                break
        # print("returning")
        return bestVal
        

    def AI_variable_depth(self):
        # self.AI_heuristic()
        sc.onclick(None)
        self.change_turn()
        self.ai_turn = True
        print("AI TURN USING HEURISTIC")

        ret = self.evaluate_variable(4, Piece.Black)
        print("Value:",ret[0])
        print("Leaves Reached:", self.leaves_reached)
        self.move_piece(ret[1], ret[2])

        for stamp in self.stamp_ids:
            tr.clearstamp(stamp)

        self.update_pieces()
        self.change_turn()
        self.ai_turn = False

        # for square in self.squares:
        #     print(square, square.castle)

        sc.onclick(self.start_square)

    def AI_heuristic(self):
        self.AI_turn_random()
        # sc.onclick(None)
        # self.change_turn()
        # self.ai_turn = True
        # print("AI TURN USING HEURISTIC")

        # # all_moves = []
        # # for square in self.squares:
        # #     if square.color == Piece.Black and square.valid_moves:
        # #         all_moves.append([square, square.valid_moves])
        # ret = self.evaluate_ai_moves()

        # if len(ret) != 0:
        #     move = random.randint(0,len(ret)-1)
        #     self.move_piece(ret[move][0],ret[move][1])


        # for stamp in self.stamp_ids:
        #     tr.clearstamp(stamp)

        # self.update_pieces()
        # self.change_turn()
        # self.ai_turn = False

        # # for square in self.squares:
        # #     print(square, square.castle)

        # sc.onclick(self.start_square)

    def AI_turn_random(self):
        sc.onclick(None)
        self.change_turn()
        self.ai_turn = True
        print("AI TURN")
        all_moves = []

        # for testing promote 
        # random.seed("pissing")

        for square in self.squares:
            if square.color == Piece.Black and square.valid_moves:
                all_moves.append([square, square.valid_moves])

        length = len(all_moves)
        if length != 0:
            src_ind = random.randint(0, length-1)
            src = all_moves[src_ind][0]

            dst_ind = random.randint(0, len(all_moves[src_ind][1])-1)
            dst = all_moves[src_ind][1][dst_ind]

        self.move_piece(src, dst)

        for stamp in self.stamp_ids:
            tr.clearstamp(stamp)

        self.update_pieces()
        self.change_turn()
        self.ai_turn = False
        sc.onclick(self.start_square)

    def game_over(self):
        self.time_end = time.perf_counter()
        tr.penup()
        tr.goto(0,0)
        tr.pendown()
        tr.shape("square")
        tr.shapesize(15,15,3)
        tr.color("#f5edb8")
        tr.pencolor('black')
        tr.stamp()
        tr.goto(0,-25)
        tr.color('#591015')
        if self.turn_color == Piece.White:
            writetext = "Black Wins!"
        else:
            writetext = "White Wins!"
        tr.write(writetext, True, align="center", font=('Arial', 30, 'italic'))
        sc.onclick(None)
        sc.onclick(None,3)
        sc.onkeypress(None,'z')

        print("-----Game Stats-----")
        print("Total Time: {}".format(math.ceil(self.time_end-self.time_start)))
        print("White Made {} Moves.".format(self.white_moves))
        print("White Captured {} Black Pieces.".format(self.white_captured))
        print("Black Made {} Moves.".format(self.black_moves))
        print("Black Captured {} White Pieces.".format(self.black_captured))

    # function for exiting game
    # called when "t" is pressed
    def exit_game(self):
        sc.bye()

    def restart_game(self):
        turn_tr.undo()
        new_game()

# main game function
def new_game():
    # sets up the turtle screen 
    # tracer set to 0 so that that pesky turtle is kept out of sight
    sc.setup(width=1200, height=1000)
    sc.tracer(0,0)
    tr.speed('fastest')
    tr.ht()
    # undo buffer in order to undo things if needed
    tr.setundobuffer(10000)
    turn_tr.hideturtle()
    turn_tr.setundobuffer(1000)

    # board is where most of the functions take place
    b = Board()
    # the board is drawn at the beginning based off the global starting fen string
    b.draw_board()
    b.load_from_fen(base_fen)
    # b.load_from_fen(time_test_fen)
    b.update_pieces()
    b.draw_promos()

    b.white_turn = False
    b.change_turn()

    # time testing code

    # t1 = time.perf_counter()
    # t3 = 0
    # t4 = 0
    # t5 = 0
    # t6 = 0
    # for i in range(1000):
    #     t5 += time.perf_counter()
    #     b.generate_all_moves(Piece.White)
    #     t6 += time.perf_counter()
    #     t3 += time.perf_counter()
    #     b.check_for_check(Piece.White)
    #     t4 += time.perf_counter()
    # t2 = time.perf_counter()
    # print("total time:", t2-t1)
    # print("mean total time:", (t2-t1)/100, "\n")
    # print("mean generate time:", (t6-t5)/100)
    # print("total generate time:", t6-t5, "\n")
    # print("mean check time:", (t4-t3)/100)
    # print("total check time:", t4-t3, "\n")
    # return

    # b.evaluate_variable(4, Piece.White)
    # print(b.leaves_reached)
    # return

    # listen for any key/button events
    # "r" restarts the game, bringing the board back to the beginning
    # "t" closes the screen and shuts down the program nicely
    # mb1 starts the main loop of the game
    sc.listen()
    sc.onkeypress(b.restart_game, "r")
    sc.onkeypress(b.exit_game, "q")
    sc.onkeypress(b.undo_move_piece, "z")
    sc.onclick(b.start_square)
    b.time_start = time.perf_counter()
    sc.mainloop()

# main duh
def main():
    # call the main game function
    # this is here in order to easily restart the game when wanted
    new_game()

if __name__ == '__main__':
    main()
