import turtle, math, copy, time, random
from piece import Piece
from move import Move
import chess

DEPTH = 3

tr = turtle.Turtle()
sc = tr.getscreen()
turn_tr = turtle.Turtle()

turn_tr_pos = {
    Piece.White: [425, -385,["White Turn!", True, "left", ('Arial', 20, 'italic', 'underline')]],
    Piece.Black: [425, 365,["Black Turn!", True, "left", ('Arial', 20, 'italic', 'underline')]],
    "promote": [425, 0,["Promoting!", True, "left", ('Arial', 20, 'italic', 'underline')]]
}

RIGHT_CLICK = 3

class Board:
    def __init__(self, mode, ver):
        # board representation
        self.startx = -400
        self.starty = 400
        self.board = [0] * 64
        self.old_board = [0] * 64
        self.stamps = [0] * 64
        self.stamp_ids = []
        self.display_color = [0] * 64
        self.first_update = True
        self.pieces_taken = []

        # ai and mode info
        self.ai_ver = ver
        self.mode = mode
        self.best_promote_piece = Piece.Queen
        self.ai_turn = False

        # move info
        self.selected_index = None
        self.selected_moves = []
        self.all_moves = []
        self.last_moves = []
        self.turn_color = Piece.White
        self.king_castle = {
            Piece.King|Piece.White: True, 
            Piece.King|Piece.Black: True
        }
        self.rook_castle = {
            0: True,
            7: True,
            56: True,
            63: True
        }
        self.total_available_moves = 0
        self.mid_game = True
        self.capture_moves = []

        # stat stuff
        self.white_moves = 0
        self.black_moves = 0
        self.white_captured = 0
        self.black_captured = 0
        self.time_start = 0
        self.time_end = 0
        self.leaves_reached = 0

        ## Not Used
        self.move_path = []

        for key in Piece.piece_map:
            sc.register_shape(Piece.piece_map[key])

    # draws the initial board
    # fairly self explanatory
    def draw_board(self):
        white = True;
        for rank in range(8):
            for file in range(8):
                tr.penup()
                x = self.startx+(file*100)
                y = self.starty-(rank*100)
                tr.setpos(x, y)
                tr.pendown()
                if white:
                    tr.fillcolor("#f5edb8")
                    self.display_color[rank*8+file] = '#A6A17C'
                else:
                    tr.fillcolor('#b3202a')
                    self.display_color[rank*8+file] = '#591015'
                tr.begin_fill()
                for i in range(4):
                    tr.forward(100)
                    tr.right(90)
                tr.end_fill()
                white = not white
            white = not white 
        sc.update()

    # loads a board state from a fen string
    # a fen string is a string that represents a board state
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
                    ptype = Piece.fen_map[ch.lower()]
                    self.board[rank*8+file] = ptype | color
                    self.old_board[rank*8+file] = ptype|color
                    file += 1
    
    # updates the board representation when needed
    # doesn't do redundant work
    def update_pieces(self):
        # iterates through the board
        for rank in range(8):
            for file in range(8):
                index = rank*8+file
                # checks if the piece needs to be updateds
                curr_piece = self.board[index]
                old_piece = self.old_board[index]
                if self.first_update or old_piece != curr_piece:
                    self.old_board[index] = curr_piece
                    tr.clearstamp(self.stamps[index])
                    if curr_piece != 0:
                        tr.shape(Piece.piece_map[curr_piece])
                        tr.penup()
                        tr.setpos(self.startx+(file*100)+50, self.starty-(rank*100)-50)
                        tr.pendown()
                        self.stamps[index] = tr.stamp() 
                    if curr_piece == 0:
                        self.stamps[index] = 0
        sc.update()
        self.first_update = False

    def switch_turn_turtle(self, promoted=False):
        turn_tr.undo()
        if self.last_moves and self.last_moves[-1].promote and not promoted:
            args = turn_tr_pos["promote"]
        else:
            args = turn_tr_pos[self.turn_color]
        turn_tr.penup()
        turn_tr.goto(args[0],args[1])
        turn_tr.color('black')
        turn_tr.pendown()
        turn_tr.write(*args[2])

    # draws the promotion graphic to the left of the board
    def draw_promos(self):
        white = False
        tr.penup()
        x,y = self.startx-100,self.starty-50
        tr.goto(x, y+75)
        tr.write("Promotions", True, align="center", font=('Arial', 20, 'normal'))
        for key, value in Piece.promo_map.items():
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

    def promote_piece(self, x=0, y=0):
        if not self.ai_turn:
            print('inside promote_helper')
            valid = False
            sc.onkeypress(None, "z")
            for key,value in Piece.promo_map.items():
                if (value[0] <= x <= value[0]+100) and (value[1] >= y >= value[1]-100):
                    self.board[self.last_moves[-1].dst] = key|(self.last_moves[-1].src_p&24)
                    valid = True
                    self.update_pieces()
            if valid:
                self.change_turn(promoted=True)
                if self.mode == 'ai':
                    if self.ai_turn:
                        sc.onclick(None)
                        self.ai_play()

        else:
            self.board[self.last_moves[-1].dst] = Piece.Queen|Piece.Black
            self.change_turn(promoted=True)

    # puts overlay on board for possible moves
    def display_possible_moves(self):
        tr.penup()
        for move in self.selected_moves:
            tr.shape('square')
            tr.color(self.display_color[move.dst])
            tr.shapesize(5, 5, 1)
            tr.shapesize(outline=2)
            tr.pencolor('black')
            rank = move.dst//8
            file = move.dst%8
            lx, ty = self.startx+(file*100), self.starty-(rank*100)
            tr.goto(lx+50, ty-50)
            self.stamp_ids.append(tr.stamp())
            if move.dst_p != Piece.Nothing:
                tr.shape(Piece.piece_map[move.dst_p])
                self.stamp_ids.append(tr.stamp())
        sc.update()

    # checks for the possibility of castling
    # updates valid moves if so
    def check_castle(self, src_ind, moves):
        src = self.board[src_ind]
        k_c = self.king_castle[src]
        if self.king_castle[src]:
            if self.board[src_ind+1] == Piece.Nothing and self.board[src_ind+2] == Piece.Nothing:
                if self.board[src_ind+3] == (self.turn_color|Piece.Rook) and self.rook_castle[src_ind+3]:
                    r_c = [src_ind+3, self.rook_castle[src_ind+3]]
                    moves.append(Move(src_ind, src_ind+2, src, self.board[src_ind+2], castle=[src_ind+3,src_ind+1, self.king_castle], king_c=k_c, rook_c=r_c))
            if ((self.board[src_ind-1] == Piece.Nothing) and (self.board[src_ind-2] == Piece.Nothing) and (self.board[src_ind-3] == Piece.Nothing)):
                if self.board[src_ind-4] == (self.turn_color|Piece.Rook) and self.rook_castle[src_ind-4]:
                    r_c = [src_ind-4, self.rook_castle[src_ind-4]]
                    moves.append(Move(src_ind, src_ind-2, src, self.board[src_ind-2], castle=[src_ind-4,src_ind-1, self.king_castle], king_c=k_c, rook_c=r_c))

    # finds the possible moves for a pawn
    # and adds them to valid moves
    def check_pawn(self, src_ind, moves):
        i = -1
        if self.turn_color == Piece.Black:
            i = 1

        dst_ind = src_ind+8*i
        src = self.board[src_ind]
        op_color = Piece.color_relation[self.turn_color][2]
        if (0 <= dst_ind <= 63):
            dst = self.board[dst_ind]
            if (dst == Piece.Nothing):
                if (0 <= dst_ind <= 7) or (56 <= dst_ind <= 63):
                    moves.append(Move(src_ind, dst_ind, src, dst, promote=True))
                else:
                    moves.append(Move(src_ind, dst_ind, src, dst))
                dst_ind = src_ind+16*i
                if ((48 <= src_ind <= 55) or (8 <= src_ind <= 15)) and (0 <= dst_ind <= 63):
                    dst = self.board[dst_ind]
                    if dst == Piece.Nothing:
                        moves.append(Move(src_ind, dst_ind, src, dst, double=True))
        
        dst_ind = src_ind+7*i
        if ((dst_ind)//8) == ((src_ind//8)+1*i) and (0 <= dst_ind <= 63):
            dst = self.board[dst_ind]
            if (dst&24) == op_color:
                if (0 <= dst_ind <= 7) or (56 <= dst_ind <= 63):
                    move = Move(src_ind, dst_ind, src, dst, promote=True)
                    moves.append(move)
                    self.capture_moves.append(move)
                else:
                    move = Move(src_ind, dst_ind, src, dst)
                    moves.append(move)
                    self.capture_moves.append(move)
            else:
                if self.last_moves:
                    if dst == Piece.Nothing and self.last_moves[-1].double:
                        if self.last_moves[-1].src == (dst_ind+8*i):
                            moves.append(Move(src_ind, dst_ind, src, dst, en_passant=[dst_ind+8*i*-1,op_color|Piece.Pawn]))
            
        dst_ind = src_ind+9*i
        if ((dst_ind)//8) == ((src_ind//8)+1*i) and (0 <= dst_ind <= 63):
            dst = self.board[dst_ind]
            if (dst&24) == op_color:
                if (0 <= dst_ind <= 7) or (56 <= dst_ind <= 63):
                    move = Move(src_ind, dst_ind, src, dst, promote=True)
                    moves.append(move)
                    self.capture_moves.append(move)
                else:
                    move = Move(src_ind, dst_ind, src, dst)
                    moves.append(move)
                    self.capture_moves.append(move)
            else:
                if self.last_moves:
                    if dst == Piece.Nothing and self.last_moves[-1].double:
                        if self.last_moves[-1].src == (dst_ind+8*i):
                            moves.append(Move(src_ind, dst_ind, src, dst, en_passant=[dst_ind+8*i*-1,op_color|Piece.Pawn]))

    # finds the possible moves for a knight
    # and adds them to valid moves
    def check_knight(self, src_ind, moves):
        src = self.board[src_ind]
        m8 = src_ind%8
        op_color = Piece.color_relation[self.turn_color][2]

        dst_ind = src_ind+17
        if (dst_ind) < 64 and (m8) != 7:
            dst = self.board[dst_ind]
            if dst == Piece.Nothing:
                moves.append(Move(src_ind, dst_ind, src, dst))
            elif dst&op_color == op_color:
                move = Move(src_ind, dst_ind, src, dst)
                moves.append(move)
                self.capture_moves.append(move)
        dst_ind = src_ind+15
        if (dst_ind) < 64 and (m8) != 0:
            dst = self.board[dst_ind]
            if dst == Piece.Nothing:
                moves.append(Move(src_ind, dst_ind, src, dst))
            elif dst&op_color == op_color:
                move = Move(src_ind, dst_ind, src, dst)
                moves.append(move)
                self.capture_moves.append(move)
        dst_ind = src_ind+6
        if (dst_ind) < 64 and (m8) > 1:
            dst = self.board[dst_ind]
            if dst == Piece.Nothing:
                moves.append(Move(src_ind, dst_ind, src, dst))
            elif dst&op_color == op_color:
                move = Move(src_ind, dst_ind, src, dst)
                moves.append(move)
                self.capture_moves.append(move)
        dst_ind = src_ind+10
        if (dst_ind) < 64 and (m8) < 6:
            dst = self.board[dst_ind]
            if dst == Piece.Nothing:
                moves.append(Move(src_ind, dst_ind, src, dst))
            elif dst&op_color == op_color:
                move = Move(src_ind, dst_ind, src, dst)
                moves.append(move)
                self.capture_moves.append(move)
        dst_ind = src_ind-15
        if (dst_ind) >= 0 and (m8) != 7:
            dst = self.board[dst_ind]
            if dst == Piece.Nothing:
                moves.append(Move(src_ind, dst_ind, src, dst))
            elif dst&op_color == op_color:
                move = Move(src_ind, dst_ind, src, dst)
                moves.append(move)
                self.capture_moves.append(move)
        dst_ind = src_ind-17
        if (dst_ind) >= 0 and (m8) != 0:
            dst = self.board[dst_ind]
            if dst == Piece.Nothing:
                moves.append(Move(src_ind, dst_ind, src, dst))
            elif dst&op_color == op_color:
                move = Move(src_ind, dst_ind, src, dst)
                moves.append(move)
                self.capture_moves.append(move)
        dst_ind = src_ind-6
        if (dst_ind) >= 0 and (m8) < 6:
            dst = self.board[dst_ind]
            if dst == Piece.Nothing:
                moves.append(Move(src_ind, dst_ind, src, dst))
            elif dst&op_color == op_color:
                move = Move(src_ind, dst_ind, src, dst)
                moves.append(move)
                self.capture_moves.append(move)
        dst_ind = src_ind-10
        if (dst_ind) >= 0 and (m8) > 1:
            dst = self.board[dst_ind]
            if dst == Piece.Nothing:
                moves.append(Move(src_ind, dst_ind, src, dst))
            elif dst&op_color == op_color:
                move = Move(src_ind, dst_ind, src, dst)
                moves.append(move)
                self.capture_moves.append(move)

    # checks if dist number squares in both vertical directions
    # can be moved to and adds them to valid moves if so
    def check_vertical(self, dist, src_ind, moves):
        src = self.board[src_ind]
        if src&7 == Piece.King:
            k_c = self.king_castle[src]
        else:
            k_c = False
        if src&7 == Piece.Rook and (src_ind in self.rook_castle.keys()):
            r_c = [src_ind, self.rook_castle[src_ind]]
        else:
            r_c = False
        for i in range(1, dist+1):
            dst_ind = src_ind+i*8
            if (dst_ind) > 63:
                break
            dst = self.board[dst_ind]
            if dst&self.turn_color == self.turn_color:
                break
            if dst == Piece.Nothing:
                moves.append(Move(src_ind, dst_ind, src, dst, king_c=k_c, rook_c=r_c))
            else:
                move = Move(src_ind, dst_ind, src, dst, king_c=k_c)
                moves.append(move)
                self.capture_moves.append(move)
                break
        for i in range(1, dist+1):
            dst_ind = src_ind-i*8
            if (dst_ind) < 0:
                break
            dst = self.board[dst_ind]
            if dst&self.turn_color == self.turn_color:
                break
            if dst == Piece.Nothing:
                moves.append(Move(src_ind, dst_ind, src, dst, king_c=k_c, rook_c=r_c))
            else:
                move = Move(src_ind, dst_ind, src, dst, king_c=k_c)
                moves.append(move)
                self.capture_moves.append(move)
                break

    # checks if dist number squares in both horizontal directions
    # can be moved to and adds them to valid moves if so
    def check_horizontal(self, dist, src_ind, moves):
        src = self.board[src_ind]
        if src&7 == Piece.King:
            k_c = self.king_castle[src]
        else:
            k_c = False
        if src&7 == Piece.Rook and (src_ind in self.rook_castle.keys()):
            r_c = [src_ind, self.rook_castle[src_ind]]
        else:
            r_c = False
        for i in range(1, dist+1):
            dst_ind = src_ind+i
            if ((dst_ind) > 63) or (((dst_ind)%8) == 0):
                break
            dst = self.board[dst_ind]
            if dst&self.turn_color == self.turn_color:
                break
            if dst == Piece.Nothing:
                moves.append(Move(src_ind, dst_ind, src, dst, king_c=k_c,rook_c=r_c))
            else:
                move = Move(src_ind, dst_ind, src, dst, king_c=k_c)
                moves.append(move)
                self.capture_moves.append(move)
                break

        for i in range(1, dist+1):
            dst_ind = src_ind-i
            if ((dst_ind) < 0) or (((dst_ind)%8) == 7):
                break
            dst = self.board[dst_ind]
            if dst&self.turn_color == self.turn_color:
                break
            if dst == Piece.Nothing:
                moves.append(Move(src_ind, dst_ind, src, dst, king_c=k_c,rook_c=r_c))
            else:
                move = Move(src_ind, dst_ind, src, dst, king_c=k_c)
                moves.append(move)
                self.capture_moves.append(move)
                break

    # checks if dist number squares in all diagonals
    # can be moved to and adds them to valid moves if so
    def check_diagonals(self, dist, src_ind, moves):
        # check a certain distance in each diagonal direction
        # if the index is out of bounds, break
        # if there is a same colored piece in the way, break
        # if there is an empty square, add that move
        # if there is an enemy piece, add that move then break
        src = self.board[src_ind]
        if src&7 == Piece.King:
            k_c = self.king_castle[src]
        else:
            k_c = False
        for i in range(1, dist+1):
            dst_ind = src_ind-i*7
            if (dst_ind) < 0 or ((dst_ind)%8) == 0:
                break
            dst = self.board[dst_ind]
            if dst&self.turn_color == self.turn_color:
                break
            if dst == Piece.Nothing:
                moves.append(Move(src_ind, dst_ind, src, dst, king_c=k_c))
            else:
                move = Move(src_ind, dst_ind, src, dst, king_c=k_c)
                moves.append(move)
                self.capture_moves.append(move)
                break
        for i in range(1, dist+1):
            dst_ind = src_ind-i*9
            if (dst_ind) < 0 or ((dst_ind)%8) == 7:
                break
            dst = self.board[dst_ind]
            if dst&self.turn_color == self.turn_color:
                break
            if dst == Piece.Nothing:
                moves.append(Move(src_ind, dst_ind, src, dst, king_c=k_c))
            else:
                move = Move(src_ind, dst_ind, src, dst, king_c=k_c)
                moves.append(move)
                self.capture_moves.append(move)
                break
        for i in range(1, dist+1):
            dst_ind = src_ind+i*7
            if (dst_ind) > 63 or ((dst_ind)%8) == 7:
                break
            dst = self.board[dst_ind]
            if dst&self.turn_color == self.turn_color:
                break
            if dst == Piece.Nothing:
                moves.append(Move(src_ind, dst_ind, src, dst, king_c=k_c))
            else:
                move = Move(src_ind, dst_ind, src, dst, king_c=k_c)
                moves.append(move)
                self.capture_moves.append(move)
                break
        for i in range(1, dist+1):
            dst_ind = src_ind+i*9
            if (dst_ind) > 63 or ((dst_ind)%8) == 0:
                break
            dst = self.board[dst_ind]
            if dst&self.turn_color == self.turn_color:
                break
            if dst == Piece.Nothing:
                moves.append(Move(src_ind, dst_ind, src, dst, king_c=k_c))
            else:
                move = Move(src_ind, dst_ind, src, dst, king_c=k_c)
                moves.append(move)
                self.capture_moves.append(move)
                break

    # checks for instances of check or checkmate
    def check_for_check(self, moves):
        remove_moves = []
        for move in moves:
            self.move_piece(move, test=True)
            new_moves = self.generate_all_moves()
            self.undo_move_piece(test=True)
            for o_move in new_moves:
                if move.castle:
                    if move.dst%8 == 6:
                        offset = -1
                    else:
                        offset = 1
                    if (o_move.dst == move.src) or (o_move.dst == (move.dst+offset)):
                        remove_moves.append(move)
                        break
                if o_move.dst_p == self.turn_color|Piece.King:
                    remove_moves.append(move)
                    break
        for move in remove_moves:
            moves.remove(move)
            if move in self.capture_moves:
                self.capture_moves.remove(move)
        
    # generates moves to be used in the main loop
    def generate_all_moves(self):
        # sets up for the moves
        all_moves = []
        self.capture_moves = []
        # iterates through the board
        for src in range(0, 64):
            # grabs the piece from the board index
            piece = self.board[src]
            # checks that the color of the piece is proper
            if (piece&self.turn_color) == self.turn_color:
                # isolates the piece type
                p = piece&7
                # checks which piece it is and calls the proper functions
                if p == Piece.King:
                    self.check_diagonals(1, src, all_moves)
                    self.check_horizontal(1, src, all_moves)
                    self.check_vertical(1, src, all_moves)
                    self.check_castle(src, all_moves)
                elif p == Piece.Queen:
                    self.check_diagonals(8, src, all_moves)
                    self.check_horizontal(8, src, all_moves)
                    self.check_vertical(8, src, all_moves)
                elif p == Piece.Bishop:
                    self.check_diagonals(8, src, all_moves)
                elif p == Piece.Knight:
                    self.check_knight(src, all_moves)
                elif p == Piece.Rook:
                    self.check_vertical(8, src, all_moves)
                    self.check_horizontal(8, src, all_moves)
                elif p == Piece.Pawn:
                    self.check_pawn(src, all_moves)
        return all_moves

    def reset_helper(self, x, y):
        sc.onclick(None)
        for stamp in self.stamp_ids:
            tr.clearstamp(stamp)
        self.stamp_ids = []
        sc.onclick(self.start_square)
        sc.onclick(None, RIGHT_CLICK)
        sc.onkeypress(self.undo_move_piece, "z")

    def change_turn(self, test=False, promoted=False):
        self.turn_color = Piece.color_relation[self.turn_color][2]

        values = {
            Piece.Pawn: 1, Piece.Bishop: 3, Piece.Knight: 3,
            Piece.Rook: 5, Piece.Queen: 9
        }
        total_white = 1*8 + 4*3 + 2*5 + 1*9
        total_black = total_white 
        for piece in self.pieces_taken:
            if piece&24 == Piece.White:
                total_white -= values[piece&7]
            else:
                total_black -= values[piece&7]
        if total_white <= 15 and total_black <= 15:
            self.mid_game = False

        if not test:
            self.switch_turn_turtle(promoted=promoted)
            sc.onclick(self.start_square)
            self.ai_turn = not self.ai_turn

    def undo_move_piece(self, test=False):
        sc.onkeypress(None, "z")
        if self.last_moves:
            if not test:
                sc.onclick(None)
            move = self.last_moves.pop()
            if move.dst_p != Piece.Nothing:
                self.pieces_taken.remove(move.dst_p)
                if move.dst_p&24 == Piece.Black:
                    self.white_captured -= 1
                else:
                    self.black_captured -= 1

            if move.src_p&24 == Piece.White:
                self.white_moves -= 1
            else:
                self.black_moves -= 1

            self.board[move.src] = move.src_p
            self.board[move.dst] = move.dst_p

            if move.castle:
                self.board[move.castle[0]] = (move.src_p&24)|Piece.Rook
                self.board[move.castle[1]] = 0
            
            if move.src_p&7 == Piece.King:
                self.king_castle[move.src_p] = move.king_c

            if move.rook_c:
                self.rook_castle[move.rook_c[0]] = move.rook_c[1]

            if move.en_passant:
                self.board[move.en_passant[0]] = move.en_passant[1]

            if not test:
                self.update_pieces()
            
            self.change_turn(test)
        sc.onkeypress(self.undo_move_piece, "z")

    # helper for doing work to move when castling
    def move_castle(self, move, test=False):
        self.board[move.castle[1]] = self.board[move.castle[0]]
        self.board[move.castle[0]] = 0

    # does the work to move a piece
    # updates board rep and values for the squares
    def move_piece(self, move, test=False):
        if move.castle:
            self.move_castle(move, test)

        if move.src_p&7 == Piece.King:
            self.king_castle[move.src_p] = False 

        if move.rook_c:
            self.rook_castle[move.rook_c[0]] = False

        self.last_moves.append(move)

        if move.dst_p != Piece.Nothing:
            self.pieces_taken.append(move.dst_p)
            if move.dst_p&24 == Piece.Black:
                self.white_captured += 1
            else:
                self.black_captured += 1
        
        if move.src_p&24 == Piece.White:
            self.white_moves += 1
        else:
            self.black_moves += 1

        self.board[move.dst] = move.src_p
        self.board[move.src] = 0

        if move.en_passant:
            if move.en_passant[1]&24 == Piece.White:
                self.black_captured += 1
            else:
                self.white_captured += 1
            self.board[move.en_passant[0]] = 0

        if not test:
            self.update_pieces()
        if not move.promote:
            self.change_turn(test=test)
        else:
            if not test:
                self.switch_turn_turtle()
                if self.ai_turn:
                    self.promote_piece()

    # does work for selecting the destination square after selecting a piece
    def destination_square(self, x, y):
        sc.onkeypress(None, "z")
        for rank in range(0,8):
            for file in range(0,8):
                lx, ty = self.startx+(file*100), self.starty-(rank*100)
                rx, by = lx + 100, ty - 100
                index = rank*8+file
                if (lx <= x <= rx) and (ty >= y >= by):
                    for move in self.selected_moves:
                        if move.dst == index:
                            sc.onclick(None)

                            self.selected_moves = []
                            for stamp in self.stamp_ids:
                                tr.clearstamp(stamp)
                            self.stamp_ids = []
                            self.move_piece(move)
                            sc.onclick(None, RIGHT_CLICK)
                            self.all_moves = []
                            if move.promote:
                                print("promoting")
                                sc.onclick(None)
                                sc.onclick(self.promote_piece)
                            elif self.mode == 'ai':
                                sc.onclick(None)
                                self.ai_play()
                            break

    # does work for selecting the piece to move
    def start_square(self, x=10000, y=100000):
        print("gen")
        self.all_moves = self.generate_all_moves()
        self.check_for_check(self.all_moves)
        if len(self.all_moves) == 0:
            self.game_over()
        valid = False
        sc.onkeypress(None, "z")
        sc.onkeypress(self.undo_move_piece, "z")
        # loops through the squares
        for rank in range(0, 8):
            for file in range(0, 8):
                lx, ty = self.startx+(file*100), self.starty-(rank*100)
                rx, by = lx + 100, ty - 100
                index = rank*8+file
                # checks that the coordinates passed in through the onclick are within the bounds of any square
                # and that the color of the clicked on square corresponds to the color of the current turn
                if (lx <= x <= rx) and (ty >= y >= by) and ((self.board[index]&24) == self.turn_color):
                    # prints which piece is selected
                    # some nice things for castling
                    # resets the valid_moves list
                    self.selected_index = index

                    # generates the moves for the specified piece 
                    # those moves are stored in the valid moves class attribute
                    self.selected_moves = []
                    for move in self.all_moves:
                        if move.src == index:
                            self.selected_moves.append(move)

                    # if there is at least one move, move on to the next function, otherwise, 
                    # wait for another click and restart process
                    if self.selected_moves:
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
            sc.onclick(self.reset_helper, RIGHT_CLICK)

    def evaluate(self, board, curr_move, first=None):
        self.leaves_reached += 1
        val = 0
        if curr_move.src_p&7 == Piece.King:
            val += Piece.square_values[Piece.King][board.mid_game][curr_move.dst]
        else:
            val += Piece.square_values[curr_move.src_p&7][curr_move.dst]
        for piece in board.board:
            val += Piece.values[piece]
        val += len(board.all_moves)*5*Piece.color_relation[board.turn_color][0]
        if first == None:
            return val
        else:
            return [val, first]

    def get_move_from_eval(self, moves):
        todo = []
        max_val = -math.inf
        for move in self.all_moves:
            self.move_piece(move, test=True)
            moves = self.generate_all_moves()
            self.check_for_check(moves)
            val = self.evaluate(self, move)
            self.undo_move_piece(test=True)
            if val > max_val:
                max_val = val
                todo = [move]
            elif val == max_val:
                todo.append(move)
        if len(todo) == 1:
            return todo[0]
        else:
            ind = random.randint(0, len(todo)-1)
            return todo[ind]

    def get_random_move(self, moves):
        move_ind = random.randint(0, len(moves)-1)
        move = moves[move_ind]
        return move

    def evaluate_search(self, board, curr_move, depth, alpha=-math.inf, beta=math.inf):
        if depth == 0:
            board.all_moves = board.generate_all_moves()
            board.check_for_check(board.all_moves)
            return self.evaluate(board, curr_move)
    
        all_moves = board.generate_all_moves()
        board.check_for_check(all_moves)
        if len(all_moves) == 0:
            return -math.inf
        for move in all_moves:
            board.move_piece(move, test=True)
            val = -self.evaluate_search(board, move, depth-1, -beta, -alpha)
            board.undo_move_piece(test=True)
            if val >= beta:
                return beta
            alpha = max(alpha, val)
        return alpha
        

    def get_move_from_search(self, moves, depth):
        max_val = -math.inf
        all_moves = copy.deepcopy(moves)
        board = copy.deepcopy(self)
        best_move = []
        alpha = -math.inf
        beta = math.inf
        for move in moves:
            first_move = move
            board.move_piece(move,test=True)
            val = -self.evaluate_search(board, move, depth-1, -beta, -alpha)
            board.undo_move_piece(test=False)
            if val >= beta:
                continue
            if val > alpha:
                alpha = val
                best_move = [move]
            elif val == alpha:
                best_move.append(move)
        print(self.leaves_reached)
        print(alpha)
        if len(best_move) == 1:
            return best_move[0]
        else:
            ind = random.randint(0, len(best_move)-1)
            return best_move[ind]


    def ai_play(self):
        print("AI TURN")
        self.all_moves = self.generate_all_moves()
        self.check_for_check(self.all_moves)
        if len(self.all_moves) == 0:
            self.game_over()
        
        if self.ai_ver == 1:
            print("ver 1")
            random.seed("pissing")
            move = self.get_random_move(self.all_moves)
            self.move_piece(move)
        elif self.ai_ver == 2:
            print("ver 2")
            move = self.get_move_from_eval(self.all_moves)
            self.move_piece(move)
        elif self.ai_ver == 3:
            print("ver 3")
            move = self.get_move_from_search(self.all_moves, DEPTH)
            self.move_piece(move)
        
        self.all_moves = []

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
        sc.onclick(None,RIGHT_CLICK)
        sc.onkeypress(None,'z')
        sc.onkeypress(self.exit_game, "q")

        print("-----Game Stats-----")
        print("Total Time: {}".format(math.ceil(self.time_end-self.time_start)))
        print("White Made {} Moves.".format(self.white_moves))
        print("White Captured {} Black Pieces.".format(self.white_captured))
        print("Black Made {} Moves.".format(self.black_moves))
        print("Black Captured {} White Pieces.".format(self.black_captured))

    # restarts the game by calling the new_game function
    def restart_game(self):
        turn_tr.undo()
        chess.new_game(self.mode, self.ai_ver, restart=True)

    # exits the game by closing the screen
    def exit_game(self):
        sc.bye()