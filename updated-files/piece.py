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

    # the following should be inverted in the future
    # for now, just do -index
    pawn_squares = [
        0,  0,  0,  0,  0,  0,  0,  0,
        5, 10,  10,-20,-20, 10, 10,  5,
        5, -5, -10,  0,  0,-10, -5,  5,
        0,  0,  0, 20, 20,  0,  0,  0,
        5,  5,  10, 25, 25, 10,  5,  5,
        10, 10, 20, 30, 30, 20, 10, 10,
        50, 50, 50, 50, 50, 50, 50, 50,
        0,  0,  0,  0,  0,  0,  0,  0
    ]

    knight_squares = [
        -50,-40,-30,-30,-30,-30,-40,-50,
        -40,-20,  0,  5,  5,  0,-20,-40,
        -30,  5, 10, 15, 15, 10,  5,-30,
        -30,  0, 15, 20, 20, 15,  0,-30,
        -30,  5, 15, 20, 20, 15,  5,-30,
        -30,  0, 10, 15, 15, 10,  0,-30,
        -40,-20,  0,  0,  0,  0,-20,-40,
        -50,-40,-30,-30,-30,-30,-40,-50
    ]

    bishop_squares = [
        -20,-10,-10,-10,-10,-10,-10,-20,
        -10,  5,  0,  0,  0,  0,  5,-10,
        -10, 10, 10, 10, 10, 10, 10,-10,
        -10,  0, 10, 10, 10, 10,  0,-10,
        -10,  5,  5, 10, 10,  5,  5,-10,
        -10,  0,  5, 10, 10,  5,  0,-10,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -20,-10,-10,-10,-10,-10,-10,-20
    ]

    rook_squares = [
        0,  0,  0,  5,  5,  0,  0,  0,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        5, 10, 10, 10, 10, 10, 10,  5,
        0,  0,  0,  0,  0,  0,  0,  0
    ]

    queen_squares = [
        -20,-10,-10, -5, -5,-10,-10,-20,
        -10,  0,  5,  0,  0,  0,  0,-10,
        -10,  5,  5,  5,  5,  5,  0,-10,
        0,  0,  5,  5,  5,  5,  0, -5,
        -5,  0,  5,  5,  5,  5,  0, -5,
        -10,  0,  5,  5,  5,  5,  0,-10,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -20,-10,-10, -5, -5,-10,-10,-20
    ]

    king_mid_squares = [
        20, 30, 10,  0,  0, 10, 30, 20,
        20, 20,  0,  0,  0,  0, 20, 20,
        -10,-20,-20,-20,-20,-20,-20,-10,
        -20,-30,-30,-40,-40,-30,-30,-20,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30
    ]

    king_late_squares = [
        -50,-30,-30,-30,-30,-30,-30,-50,
        -30,-30,  0,  0,  0,  0,-30,-30,
        -30,-10, 20, 30, 30, 20,-10,-30,
        -30,-10, 30, 40, 40, 30,-10,-30,
        -30,-10, 30, 40, 40, 30,-10,-30,
        -30,-10, 20, 30, 30, 20,-10,-30,
        -30,-20,-10,  0,  0,-10,-20,-30,
        -50,-40,-30,-20,-20,-30,-40,-50
    ]

    square_values = {
        Pawn: pawn_squares,
        Bishop: bishop_squares,
        Knight: knight_squares,
        Rook: rook_squares,
        Queen: queen_squares,
        King: {True: king_mid_squares, False: king_late_squares}
    }

    fen_map = {
        'k': King,
        'p': Pawn, 
        'n': Knight,
        'b': Bishop, 
        'r': Rook,
        'q': Queen
    }

    piece_map = {
        King|Black:     B_KING,
        King|White:     W_KING,
        Queen|Black:    B_QUEEN,
        Queen|White:    W_QUEEN,
        Bishop|Black:   B_BISHOP,
        Bishop|White:   W_BISHOP,
        Knight|Black:   B_KNIGHT,
        Knight|White:   W_KNIGHT,
        Rook|Black:     B_ROOK,
        Rook|White:     W_ROOK,
        Pawn|Black:     B_PAWN,
        Pawn|White:     W_PAWN,
    }

    promo_map = {
        Queen:    [0,0,W_QUEEN],
        Bishop:   [0,0,W_BISHOP],
        Knight:   [0,0,W_KNIGHT],
        Rook:     [0,0,W_ROOK]
    }