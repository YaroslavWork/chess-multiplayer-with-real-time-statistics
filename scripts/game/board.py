import chess
import pygame

class Board:

    def __init__(self, size: int, position: pygame.Vector2) -> None:
        self.board_size = size
        self.square_size = size // 8
        self.position = position
        
        self.images = {}

        self._cBoard = chess.Board()

        self.load_images('img/Pieces', 'svg')

    def load_images(self, path: str, extension: str = "png") -> None:
        self.images = {}
        pieces = ['r', 'n', 'b', 'q', 'k', 'p', 'R', 'N', 'B', 'Q', 'K', 'P']
        for piece in pieces:
            self.images[piece] = pygame.image.load(f"{path}/{piece}.{extension}")
            self.images[piece] = pygame.transform.scale(self.images[piece], (self.square_size, self.square_size))

    def draw(self, screen, debug = False):
        for x in range(8):
            for y in range(8):
                start_pos = (self.position[0] + x*self.square_size, self.position[1] + y*self.square_size)
                if (x+y) % 2 == 0:                    
                    pygame.draw.rect(screen, (238,238,210), (*start_pos, self.square_size, self.square_size))
                else:
                    pygame.draw.rect(screen, (118,150,86), (*start_pos, self.square_size, self.square_size))

        pieces = self._cBoard.piece_map()

        for square, piece in pieces.items():
            x = chess.square_file(square)
            y = 7 - chess.square_rank(square)
            start_pos = (self.position[0] + x*self.square_size, self.position[1] + y*self.square_size)
            screen.blit(self.images[piece.symbol()], start_pos)

    def click(self, mouse_pos: pygame.Vector2) -> None:
        x = (mouse_pos[0] - self.position[0]) // self.square_size
        y = (mouse_pos[1] - self.position[1]) // self.square_size
        square = chess.square(int(x), 7 - int(y))
        print(f"Clicked on square: {chess.square_name(square)}")
        print(f"Square index: {square}")