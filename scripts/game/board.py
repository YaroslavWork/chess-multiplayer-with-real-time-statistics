import chess
import pygame
from enum import Enum

from scripts.settings import IMG_PIECES_PATH, IMG_PIECES_EXTENSION, COLORS
from scripts.UI.text import Text

class PromotionStateUI(Enum):
    NOT_PROMOTING = 0
    PROMOTING = 1
    PROMOTED = 2


class Board:

    def __init__(self, size: int, position: pygame.Vector2) -> None:
        self.board_size = size
        self.square_size = size // 8
        self.position = position
        
        self.images = {}
        self.current_square_position_str = None

        self.is_clicked = False
        self.active_square_index = None
        self.counting_moves = 0

        self.promotion_state = PromotionStateUI.NOT_PROMOTING
        self.move_under_promotion = None
        self.promoted_piece = None

        self._cBoard = chess.Board()

        self.load_images(IMG_PIECES_PATH, IMG_PIECES_EXTENSION)

    def load_images(self, path: str, extension: str = "png") -> None:
        self.images = {}
        pieces = ['r', 'n', 'b', 'q', 'k', 'p', 'R', 'N', 'B', 'Q', 'K', 'P']
        for piece in pieces:
            self.images[piece] = pygame.image.load(f"{path}/{piece}.{extension}")
            self.images[piece] = pygame.transform.scale(self.images[piece], (self.square_size, self.square_size))

    def update(self, dt: float, mouse_pos: pygame.Vector2) -> None:
        square_index = self.find_square_position_by_mouse_position(mouse_pos)
        if square_index is None:
            self.current_square_position_str = None
            return
        
        # find square name like a1 or h4
        file = chess.FILE_NAMES[square_index[0]]
        rank = chess.RANK_NAMES[square_index[1]]
        self.current_square_position_str = f"{file}{rank}"

        if self.is_clicked:
            self.is_clicked = False

            if self.promotion_state == PromotionStateUI.PROMOTED:
                self.promotion_state = PromotionStateUI.NOT_PROMOTING

                move = chess.Move(*self.move_under_promotion, promotion=self.promoted_piece)
                if move in self._cBoard.legal_moves:
                    self._cBoard.push(move)
                    self.counting_moves += 1

                self.move_under_promotion = None
                self.promoted_piece = None
                return
            
            if self.active_square_index is None:
                self.active_square_index = square_index
            else:
                from_index = chess.square(self.active_square_index[0], self.active_square_index[1])
                to_index = chess.square(square_index[0], square_index[1])
                
                # --- Promotion handling ---
                piece = self._cBoard.piece_at(from_index)
                if piece is not None and piece.piece_type == chess.PAWN:
                    if (piece.color == chess.WHITE and square_index[1] == 7) or \
                        (piece.color == chess.BLACK and square_index[1] == 0):
                        self.promotion_state = PromotionStateUI.PROMOTING
                        self.move_under_promotion = (from_index, to_index)
                        return
                    else:
                        move = chess.Move(from_index, to_index)
                else:
                    move = chess.Move(from_index, to_index)

                if move in self._cBoard.legal_moves:
                    self._cBoard.push(move)
                    self.counting_moves += 1
                
                self.active_square_index = None

    def draw(self, screen, mouse_pos, debug = False):
        for x in range(8):
            for y in range(8):
                start_pos = (self.position[0] + x*self.square_size, self.position[1] + y*self.square_size)
                if (x+y) % 2 == 0:                    
                    pygame.draw.rect(screen, COLORS['light_square'], (*start_pos, self.square_size, self.square_size))
                else:
                    pygame.draw.rect(screen, COLORS['dark_square'], (*start_pos, self.square_size, self.square_size))
        # add letters and numbers around the board
        for i in range(8):
            file = chess.FILE_NAMES[i]
            rank = chess.RANK_NAMES[i]
            square_color = COLORS['dark_square'] if (i % 2 != 0) else COLORS['light_square']
            Text(text=file, color=square_color, size_font=25).print(screen,
                                                             (self.position[0] + i*self.square_size + self.square_size - 10,
                                                              self.position[1] + 8*self.square_size - 10),
                                                             center=True)
            Text(text=rank, color=square_color, size_font=25).print(screen,
                                                             (self.position[0] + 10,
                                                              self.position[1] + (7 - i)*self.square_size + 10),
                                                             center=True)
        pieces = self._cBoard.piece_map()

        for square, piece in pieces.items():
            x = chess.square_file(square)
            y = 7 - chess.square_rank(square)

            if self.active_square_index is not None and (x, 7 - y) == self.active_square_index:
                start_pos = (mouse_pos[0] - self.square_size // 2, mouse_pos[1] - self.square_size // 2)
            else:
                start_pos = (self.position[0] + x*self.square_size, self.position[1] + y*self.square_size)
            
            screen.blit(self.images[piece.symbol()], start_pos)

        if self.promotion_state == PromotionStateUI.PROMOTING:
            self.draw_promotion_UI(screen)

    def draw_promotion_UI(self, screen) -> None:
        is_white = self._cBoard.turn == chess.WHITE
        pieces = ['q', 'r', 'b', 'n'] if not is_white else ['Q', 'R', 'B', 'N']

        width_size = self.square_size * 4 + 25
        height_size = self.square_size + 10
        start_pos = (self.position[0] + (self.board_size - width_size) // 2,
                     self.position[1] + (self.board_size - height_size) // 2)
        
        pygame.draw.rect(screen, COLORS['dark_square'], (
            start_pos[0]-2, start_pos[1]-2, width_size+4, height_size+4)
        )
        pygame.draw.rect(screen, COLORS['light_square'], (*start_pos, width_size, height_size))
        
        for i, piece in enumerate(pieces):
            piece_pos = (start_pos[0] + i * self.square_size + i * 5 + 5,
                         start_pos[1] + 5)
            pygame.draw.rect(screen, COLORS['dark_square'], (
                piece_pos[0], piece_pos[1], self.square_size, self.square_size)
            )
            screen.blit(self.images[piece], piece_pos)

    def click(self, mouse_pos: pygame.Vector2) -> None:
        self.is_clicked = True

        if self.promotion_state == PromotionStateUI.PROMOTING:
            self.handle_promotion_click(mouse_pos)

    def handle_promotion_click(self, mouse_pos: pygame.Vector2) -> None:
        if self.promotion_state == PromotionStateUI.PROMOTING:
            width_size = self.square_size * 4 + 25
            height_size = self.square_size + 10
            start_pos = (self.position[0] + (self.board_size - width_size) // 2,
                         self.position[1] + (self.board_size - height_size) // 2)
            
            for i in range(4):
                piece_pos = (start_pos[0] + i * self.square_size + i * 5 + 5,
                             start_pos[1] + 5)
                rect = pygame.Rect(piece_pos[0], piece_pos[1], self.square_size, self.square_size)
                if rect.collidepoint(mouse_pos):
                    if i == 0:
                        self.promoted_piece = chess.QUEEN 
                    elif i == 1:
                        self.promoted_piece = chess.ROOK
                    elif i == 2:
                        self.promoted_piece = chess.BISHOP
                    elif i == 3:
                        self.promoted_piece = chess.KNIGHT
                    self.promotion_state = PromotionStateUI.PROMOTED
                    break

    def find_square_name_text(self) -> str | None:
        return self.current_square_position_str
    
    def find_square_position_by_mouse_position(self, mouse_pos: pygame.Vector2) -> tuple[int, int] | None:
        x = (mouse_pos[0] - self.position[0]) // self.square_size
        y = (mouse_pos[1] - self.position[1]) // self.square_size
        
        if x < 0 or x > 7 or y < 0 or y > 7:
            return None
        return int(x), int(7 - y)  # Invert y axis for chess board representation
    
    def convert_position_to_index(pos: tuple[int, int]) -> int:
        file, rank = pos
        return chess.square(file, rank)
    
    def get_board(self) -> chess.Board:
        return self._cBoard