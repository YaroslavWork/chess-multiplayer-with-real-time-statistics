import pygame

from scripts.UI.text import Text
from scripts.game.board import Board
from scripts.analysis import EngineManager
from scripts.settings import COLORS

class Statistics:

    def __init__(self, position: pygame.Vector2) -> None:
        self.position = position
        
        self.is_square_light = True
        self.current_square_position_str = None
        self.current_score_str = None
        self.current_depth_str = None

        self.square_text = Text(f"Square: {self.current_square_position_str}", (0, 0, 0), 40)
        self.score_text = Text(f"Score: {self.current_score_str}", (0, 0, 0), 20)
        self.depth_text = Text(f"Depth: {self.current_depth_str}", (0, 0, 0), 20)

    def update(self, board: Board, engine: EngineManager) -> None:
        self.current_square_position_str = board.convert_square_to_str()
        self.is_square_light = board.is_square_light(board.current_square_position) if board.current_square_position is not None else True
        self.current_score_str = engine.current_score
        self.current_depth_str = engine.current_depth
        self.white_backyard = board.white_graveyard
        self.black_backyard = board.black_graveyard

    def draw(self, screen) -> None:
        if self.current_square_position_str:
            pygame.draw.rect(
                screen,
                COLORS['light_square'] if self.is_square_light else COLORS['dark_square'],
                pygame.Rect(self.position[0], self.position[1], 50, 50)
            )
            self.square_text.update_text(self.current_square_position_str.upper())
            self.square_text.print(
                screen,
                (self.position[0]+25, self.position[1]+25),
                True
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

        Text(f"White captured: {self.white_backyard}", (0, 0, 0), 20).print(
            screen,
            (self.position[0], self.position[1] + 90),
            False
        )

        Text(f"Black captured: {self.black_backyard}", (0, 0, 0), 20).print(
            screen,
            (self.position[0], self.position[1] + 120),
            False
        )