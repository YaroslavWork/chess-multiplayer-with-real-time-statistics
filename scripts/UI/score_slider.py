import pygame

from scripts.settings import COLORS
from scripts.UI.text import Text

class ScoreSlider:

    def __init__(self, position: tuple[int, int], size: tuple[int, int], text, score = 0, loading=False) -> None:
        self.position = position
        self.size = size

        self.score = score
        self.fill = 0
        self.loading = loading

        self.loading_text = Text("Loading...", COLORS['black_piece'], self.size[1]-5)
        self.score_text = Text(text, COLORS['black_piece'], self.size[1]-5)

    def update_score(self, score: int) -> None:
        self.score = score
        self._update_fill()

    def update_text(self, text) -> None:
        self.score_text.update_text(text)

    def set_loading(self, loading: bool) -> None:
        self.loading = loading

    def _update_fill(self) -> None:
        less_than_zero = True if self.score < 0 else False
        int_number = int(abs(self.score))
        left_number = abs(self.score) - int_number

        current_fill = 0.5
        division_by = 0.5
        for _ in range(int_number):
            division_by /= 2
            current_fill += division_by

        if less_than_zero:
            current_fill = 1 - current_fill
            current_fill -= division_by / 2 * left_number
        else:
            current_fill += division_by / 2 * left_number

        self.fill = current_fill

    def draw(self, screen) -> None:
        if self.loading:
            pygame.draw.rect(screen, COLORS['white_piece'], (self.position[0], self.position[1], self.size[0], self.size[1]), 2)
            self.loading_text.print(
                screen, (self.position[0] + self.size[0] / 2, self.position[1] + self.size[1] / 2), True)
        else:
            pygame.draw.rect(screen, COLORS['white_piece'], (self.position[0], self.position[1], self.size[0], self.size[1]), 2)
            pygame.draw.rect(screen, COLORS['white_piece'], (self.position[0], self.position[1], self.size[0] * self.fill, self.size[1]))
            self.score_text.text = f"{self.score}"
            self.score_text.print(screen, (self.position[0] + 30, self.position[1] + self.size[1] // 2), True)