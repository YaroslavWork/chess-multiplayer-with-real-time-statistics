import pygame


# Class Text - represents text in the model (this class optimizes the use of fonts and a text surface
# because pygame.font.Font is very slow)
class Text:
    fonts = {}  # Dictionary of fonts

    def __init__(self, text, color, size_font, type_font=None) -> None:
        if size_font in Text.fonts:
            self.font = Text.fonts[size_font]
        else:
            if type_font:
                self.font = pygame.font.Font("fonts/" + type_font + ".ttf", size_font)
            else:
                self.font = pygame.font.Font(None, size_font)
            Text.fonts[size_font] = self.font
        self.text_surface = self.font.render(text, True, color)

    def print(self, screen, pos, center=True) -> None:
        if center:
            screen.blit(self.text_surface, self.text_surface.get_rect(center=pos))
        else:
            screen.blit(self.text_surface, pos)
