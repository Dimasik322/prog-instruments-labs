#coding:utf8
import re
from copy import deepcopy

import pieces
from pieces import Piece

START_PATTERN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w 0 1'


class Board(dict):
    """
    A class that simulates chessboard
    """
    y_axis = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H')
    x_axis = (1, 2, 3, 4, 5, 6, 7, 8)
    captured_pieces = { 'white' : [], 'black' : [] }
    player_turn = None
    halfmove_clock = 0
    fullmove_number = 1
    history = []

    def __init__(self, pat: str = None) -> None:
        """
        Initializes Board object with pattern
        pat: pattern that is needed to be set
        """
        self.show(START_PATTERN)

    def is_in_check_after_move(self, p1: str, p2: str) -> bool:
        """
        Checks King piece after move
        p1: start position
        p2: end position
        """
        tmp = deepcopy(self)
        tmp.move(p1, p2)
        return tmp.king_in_check(self[p1].color)

    def shift(self, p1: str, p2: str) -> None:
        """
        Shifts piece from start position to end position
        p1: start position of piece
        p2: end position of piece
        """
        p1, p2 = p1.upper(), p2.upper()
        piece = self[p1]
        try:
            dest  = self[p2]
        except:
            dest = None
        if self.player_turn != piece.color:
            raise NotYourTurn("Not " + piece.color + "'s turn!")
        enemy = ('white' if piece.color == 'black' else 'black' )
        moves_available = piece.moves_available(p1)
        if p2 not in moves_available:
            raise InvalidMove
        if self.all_moves_available(enemy):
            if self.is_in_check_after_move(p1, p2):
                raise Check
        if not moves_available and self.king_in_check(piece.color):
            raise CheckMate
        elif not moves_available:
            raise Draw
        else:
            self.move(p1, p2)
            self.complete_move(piece, dest, p1, p2)

    def move(self, p1: str, p2: str) -> None:
        """
        Moves piece from start position to end position
        p1: start position of piece
        p2: end position of piece
        """
        piece = self[p1]
        try:
            dest  = self[p2]
        except:
            pass
        del self[p1]
        self[p2] = piece

    def complete_move(self, piece: Piece, dest: str, p1: str, p2: str) -> None:
        """
        Moves piece to destination from start position to end position
        piece: a piece that is needed to move
        dest: destination
        p1: start position of piece
        p2: end position of piece
        """
        enemy = ('white' if piece.color == 'black' else 'black' )
        if piece.color == 'black':
            self.fullmove_number += 1
        self.halfmove_clock += 1
        self.player_turn = enemy
        abbr = piece.shortname
        if abbr == 'P':
            abbr = ''
            self.halfmove_clock = 0
        if dest is None:
            movetext = abbr +  p2.lower()
        else:
            movetext = abbr + 'x' + p2.lower()
            self.halfmove_clock = 0
        self.history.append(movetext)

    def all_moves_available(self, color: str) -> list:
        """
        Returns all available moves for piece
        color: color of side
        """
        result = []
        for coord in self.keys():
            if (self[coord] is not None) and self[coord].color == color:
                moves = self[coord].moves_available(coord)
                if moves: result += moves
        return result

    def occupied(self, color: str) -> list:
        """
        Returns all occupied cells
        color: color of side
        """
        result = []
        for coord in self.iterkeys():
            if self[coord].color == color:
                result.append(coord)
        return result

    def position_of_king(self, color: str) -> str:
        """
        Returns position of King piece
        color: color of side
        """
        for pos in self.keys():
            if isinstance(self[pos], pieces.King) and self[pos].color == color:
                return pos

    def king_in_check(self, color: str) -> bool:
        """
        Checks if King piece is in check
        color: color of side
        """
        kingpos =  self.position_of_king(color)
        opponent = ('black' if color =='white' else 'white')
        for pieces in self.iteritems():
            if kingpos in self.all_moves_available(opponent):
                return True
            else:
                return False

    def alpha_notation(self, xycoord: str) -> str:
        """
        Normilizes xy coordinates by sizes of board
        xycoords: xy coordinates
        """
        if xycoord[0] < 0 or xycoord[0] > 7 or xycoord[1] < 0 or xycoord[1] > 7: return
        return self.y_axis[xycoord[1]] + str(self.x_axis[xycoord[0]])

    def num_notation(self, coord: str) -> tuple:
        """
        Returns inverted coordinates
        coord: current coordinates
        """
        return int(coord[1]) - 1, self.y_axis.index(coord[0])

    def is_on_board(self, coord: str) -> bool:
        """
        Check if coordinates are on board
        coords: coordinates which are needed to check
        """
        if coord[1] < 0 or coord[1] > 7 or coord[0] < 0 or coord[0] > 7:
            return False
        else: return True

    def show(self, pat: str) -> None:
        """
        Shows Board in current state
        pat: pattern of board
        """
        self.clear()
        pat = pat.split(' ')
        def expand(match): return ' ' * int(match.group(0))
        pat[0] = re.compile(r'\d').sub(expand, pat[0])
        for x, row in enumerate(pat[0].split('/')):
            for y, letter in enumerate(row):
                if letter == ' ': continue
                coord = self.alpha_notation((7 - x, y))
                self[coord] = pieces.create_piece(letter)
                self[coord].place(self)
        if pat[1] == 'w': self.player_turn = 'white'
        else: self.player_turn = 'black'
        self.halfmove_clock = int(pat[2])
        self.fullmove_number = int(pat[3])


class ChessError(Exception): pass
class Check(ChessError): pass
class InvalidMove(ChessError): pass
class CheckMate(ChessError): pass
class Draw(ChessError): pass
class NotYourTurn(ChessError): pass
class InvalidCoord(ChessError): pass
 