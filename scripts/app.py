import pygame
import threading

import scripts.settings as s
from scripts.camera import Camera
from scripts.field import Field
from scripts.UI.text import Text

from scripts.game.board import Board
from scripts.game.statistics import Statistics
from scripts.analysis import EngineManager
from scripts.notification import Notification

class App:

    def __init__(self) -> None:
        # Initialize pygame and settings
        pygame.init()

        self.size = self.width, self.height = s.SIZE
        self.name = s.NAME
        self.colors = s.COLORS
        self.fps = s.FPS

        # Set pygame window
        pygame.display.set_caption(self.name)

        # Set pygame clock
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()

        # Set input variables
        self.dt = 0
        self.mouse_pos = (0, 0)
        self.keys = []

        # Set model variables
        self.camera = Camera(x=0, y=0, distance=10, resolution=self.size)
        # This line takes data from save file
        self.field = Field()
        # sprites
        self.sprites = {}
        self.load_group_images('Pieces')

        # Game attributes
        self.current_move = 0 # check to update analysis

        self.board = Board(720, (0, 0), self.sprites['Pieces'])
        self.statistics = Statistics((730, 10), self.sprites['Pieces'])
        
        self.engine = EngineManager(s.ENGINE_PATH)
        self.engine.start_analysis(board = self.board.get_board())

    def load_group_images(self, group_name: str) -> None:
        self.sprites = {}
        for image_name in s.IMAGES[f'img/{group_name}']:
            image_path = f'img/{group_name}/{image_name}'
            image = pygame.image.load(image_path).convert_alpha()
            if group_name not in self.sprites:
                self.sprites[group_name] = {}
            self.sprites[group_name][image_name.split('.')[0]] = image
        print(f'Loaded image: {self.sprites}')
    
    def update(self) -> None:
        """
        Main update function of the program.
        This function is called every frame
        """

        # -*-*- Input Block -*-*-
        self.mouse_pos = pygame.mouse.get_pos()  # Get mouse position

        for event in pygame.event.get():  # Get all events
            if event.type == pygame.QUIT:  # If you want to close the program...
                close()
                Text.fonts = {}  # Clear fonts

            if event.type == pygame.MOUSEBUTTONDOWN:  # If mouse button down...
                if event.button == 1:
                    self.board.click(self.mouse_pos)
                elif event.button == 3:
                    pass

            if event.type == pygame.KEYDOWN:  # If key button down...
                if event.key == pygame.K_SPACE:
                    pass

        # -*-*- Physics Block -*-*-
        self.board.update(self.dt, self.mouse_pos)
        self.statistics.update(self.board, self.engine)
        if self.current_move != self.board.counting_moves:
            self.current_move = self.board.counting_moves
            self.engine.start_analysis(board = self.board.get_board())
        
        for notification in Notification.INSTANCES:
            notification.update(self.dt)
        # -*-*-               -*-*-

        # -*-*- Rendering Block -*-*-
        self.screen.fill(self.colors['background'])  # Fill background

        self.board.draw(self.screen, self.mouse_pos)
        self.statistics.draw(self.screen)

        for notification in Notification.INSTANCES:
            notification.draw(self.screen, self.mouse_pos)

        Text("FPS: " + str(int(self.clock.get_fps())), (0, 0, 0), 20).print(self.screen,
                                                                            (self.width - 60, self.height - 14),
                                                                            False)  # FPS counter
        # -*-*-                 -*-*-

        # -*-*- Update Block -*-*-
        pygame.display.update()

        self.dt = self.clock.tick(self.fps)
        # -*-*-              -*-*-


def close():
    pygame.quit()
    exit()
