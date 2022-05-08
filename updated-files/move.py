class Move:
    def __init__(self, src_ind, dst_ind, src_piece, dst_piece, en_passant=False, castle=False, promote=False, double=False, king_c=False, rook_c=False):
        self.src = src_ind
        self.dst = dst_ind
        self.src_p = src_piece
        self.dst_p = dst_piece
        self.en_passant = en_passant
        self.castle = castle
        self.promote = promote
        self.double = double
        self.king_c = king_c
        self.rook_c = rook_c

    def __str__(self):
        return "sind: {}, dind: {}, sp: {}, dp: {}, ep: {}, c: {}, p: {}, d: {}".format(
            self.src,self.dst, self.src_p, self.dst_p, 
            self.en_passant, self.castle, self.promote, self.double
        )