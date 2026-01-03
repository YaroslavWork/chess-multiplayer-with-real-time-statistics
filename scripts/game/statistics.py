import pygame

from scripts.UI.text import Text
from scripts.game.board import Board
from scripts.analysis import EngineManager

class Statistics:

    def __init__(self, position: pygame.Vector2) -> None:
        self.position = position
        self.current_square_position_str = None
        self.current_score_str = None
        self.current_depth_str = None

        self.square_text = Text(f"Square: {self.current_square_position_str}", (0, 0, 0), 20)
        self.score_text = Text(f"Score: {self.current_score_str}", (0, 0, 0), 20)
        self.depth_text = Text(f"Depth: {self.current_depth_str}", (0, 0, 0), 20)

    def update(self, board: Board, engine: EngineManager) -> None:
        self.current_square_position_str = board.find_square_name_text()
        self.current_score_str = engine.current_score
        self.current_depth_str = engine.current_depth

    def draw(self, screen) -> None:
        if self.current_square_position_str:
            self.square_text.update_text(f"Square: {self.current_square_position_str}")
            self.square_text.print(
                screen,
                (self.position[0], self.position[1]),
                False
            )

        if self.current_score_str:
            if self.current_score_str.startswith("#"):
                score_text = f"Mate in {self.current_score_str[2:]}"
            else:
                score_text = f"Score: {self.current_score_str}"

            self.score_text.update_text(score_text)
            self.score_text.print(
                screen,
                (self.position[0], self.position[1] + 30),
                False
            )
            
        if self.current_depth_str:
            self.depth_text.update_text(f"Depth: {self.current_depth_str}")
            self.depth_text.print(
                screen,
                (self.position[0], self.position[1] + 60),
                False
            )