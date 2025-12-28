import pygame

from scripts.UI.text import Text
from scripts.game.board import Board

class Statistics:

    def __init__(self, position: pygame.Vector2) -> None:
        self.position = position
        self.current_square_position_str = None

    def update(self, board: Board) -> None:
        self.current_square_position_str = board.find_square_name_text()

    def draw(self, screen) -> None:
        if self.current_square_position_str:
            Text(f"Square: {self.current_square_position_str}", (0, 0, 0), 20).print(
                screen,
                (self.position[0], self.position[1]),
                False
            )