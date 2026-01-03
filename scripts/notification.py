import pygame
from scripts.UI.text import Text
from scripts.settings import COLORS

class Notification:
    INSTANCES = []

    def __init__(self, message: str, amount_of_time: float) -> None:
        self.message = message
        self.amount_of_time = amount_of_time
        self.start_time = pygame.time.get_ticks() / 1000.0  # Convert to seconds
        Notification.INSTANCES.append(self)

    def update(self, dt: float) -> bool:
        current_time = pygame.time.get_ticks() / 1000.0  # Convert to seconds
        if current_time - self.start_time >= self.amount_of_time:
            Notification.INSTANCES.remove(self)
    
    def draw(self, screen: pygame.Surface, mouse_pos: pygame.Vector2) -> None:
        width_size = 150
        height_size = 40
        start_pos = (mouse_pos[0] + 10,
                     mouse_pos[1] - height_size - 10)
        center_pos = (start_pos[0] + width_size / 2,
                      start_pos[1] + height_size / 2)
        pygame.draw.rect(screen, COLORS['dark_square'], (
            start_pos[0]-2, start_pos[1]-2, width_size+4, height_size+4)
        )
        pygame.draw.rect(screen, COLORS['light_square'], (*start_pos, width_size, height_size))
        Text(self.message, COLORS['check_highlight'], 22).print(screen, center_pos, True)