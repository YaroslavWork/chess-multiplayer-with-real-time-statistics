import pygame

from scripts.UI.text import Text
from scripts.game.board import Board
from scripts.analysis import EngineManager
from scripts.settings import COLORS
from scripts.UI.score_slider import ScoreSlider

class Statistics:

    def __init__(self, position: pygame.Vector2, size: pygame.Vector2, piece_sprite: pygame.Surface) -> None:
        self.position = position
        self.size = size
        self.piece_sprite = piece_sprite

        self.is_square_light = True
        self.current_square_position_str = None
        self.current_score = None
        self.current_depth = None

        self.square_text = Text(f"Square: {self.current_square_position_str}", (0, 0, 0), 40)
        self.score_text = Text(f"Score: {self.current_score}", (0, 0, 0), 20)
        self.depth_text = Text(f"Depth: {self.current_depth}", (0, 0, 0), 20)

        self.score_slider = ScoreSlider(
            position=(self.position[0]+70, self.position[1]),
            size=(self.size[0]-90, 60), text='-'
        )
        
        self.transform_sprite_sizes(50)
        
    def transform_sprite_sizes(self, size: int) -> None:
        for key in self.piece_sprite:
            self.piece_sprite[key] = pygame.transform.scale(self.piece_sprite[key], (size, size))


    def update(self, board: Board, engine: EngineManager) -> None:
        self.current_square_position_str = board.convert_square_to_str()
        self.is_square_light = board.is_square_light(board.current_square_position) if board.current_square_position is not None else True
        self.current_score = engine.current_score
        self.current_depth = engine.current_depth
        self.white_backyard = board.white_graveyard
        self.black_backyard = board.black_graveyard

        score = float(self.current_score) if self.current_score[1] != 'M' else 0
        if self.current_score[0] == '+':
            score = 10
        elif self.current_score[0] == '-':
            score = -10
        self.score_slider.update_score(score)
        self.score_slider.update_text(self.current_score)

    def draw(self, screen) -> None:
        self.draw_square_identifier(screen, (0, 0), 60)
        self.draw_score_information(screen)
        self.draw_graveyards(screen, (0, 140), (self.size[0]-50, 50))

        

    def draw_square_identifier(self, screen, position: pygame.Vector2, square_size: int) -> None:
        if self.current_square_position_str:
            colors = COLORS['light_square'] if self.is_square_light else COLORS['dark_square']
            self.square_text.update_text(self.current_square_position_str.upper())
        else:
            colors = COLORS['light_square']
            self.square_text.update_text("--")

        relative_position = (self.position[0]+position[0], self.position[1]+position[1])
        pygame.draw.rect(
            screen,
            colors,
            pygame.Rect(*relative_position, square_size, square_size)
        )
        self.square_text.print(
            screen,
            (relative_position[0]+square_size//2, relative_position[1]+square_size//2),
            True
        )

    def draw_score_information(self, screen) -> None:
        if self.current_depth >= 25:
            self.score_slider.set_loading(False)
        else:
            self.score_slider.set_loading(True)
        self.score_slider.draw(screen)

    def draw_graveyards(self, screen, position: pygame.Vector2, size: pygame.Vector2) -> None:
        relative_position = (self.position[0]+position[0], self.position[1]+position[1])
        
        for i in range(len(self.white_backyard)):
            piece_pos = (relative_position[0] + i * 15, relative_position[1] / 2)
            screen.blit(
                self.piece_sprite[self.white_backyard[i]], piece_pos
            )

        for i in range(len(self.black_backyard)):
            piece_pos = (relative_position[0] + size[0] - i * 15, relative_position[1] / 2)
            screen.blit(
                self.piece_sprite[self.black_backyard[i]], piece_pos
            )