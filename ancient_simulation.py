import pygame
import sys
import math

import ancient_config as config
from ancient_drawing import AncientRenderer
from ancient_back_face import AncientBackRenderer

class AncientSimulationState:
    """Manages the state of the ancient simulation."""
    def __init__(self):
        self.current_day = 0
        self.time_multiplier = 1.0
        self.paused = False
        self.body_angles = {name: 0 for name in config.GEOCENTRIC_DATA}

    def update(self):
        if not self.paused:
            self.current_day += self.time_multiplier
            self._update_body_angles()

    def _update_body_angles(self):
        for name, data in config.GEOCENTRIC_DATA.items():
            angle = (self.current_day / data['period']) * 2 * math.pi
            self.body_angles[name] = angle

    def change_speed(self, factor):
        self.time_multiplier *= factor

    def toggle_pause(self):
        self.paused = not self.paused

class AncientAntikythera:
    """Main application class for the ancient simulation."""
    def __init__(self):
        pygame.init()
        self._setup_screen()
        self._load_fonts()

        self.state = AncientSimulationState()
        self.front_renderer = AncientRenderer(self.screen, self.fonts)
        self.back_renderer = AncientBackRenderer(self.screen, self.fonts)
        self.current_view = 'front'
        self.clock = pygame.time.Clock()

    def _setup_screen(self):
        info = pygame.display.Info()
        screen_height = info.current_h
        self.WIDTH = self.HEIGHT = min(config.MAX_WIDTH, screen_height - config.SCREEN_HEIGHT_ADJUST)
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Ancient Antikythera - Geocentric View")

    def _load_fonts(self):
        self.fonts = {
            'small': pygame.font.SysFont('serif', int(self.WIDTH / 70)),
            'medium': pygame.font.SysFont('serif', int(self.WIDTH / 60)),
            'large': pygame.font.SysFont('serif', int(self.WIDTH / 45), bold=True),
            'planet': pygame.font.SysFont('serif', int(self.WIDTH / 75)),
            'zodiac': pygame.font.SysFont('serif', int(self.WIDTH / 55)),
        }

    def run(self):
        """Main simulation loop."""
        while True:
            self._handle_input()
            self.state.update()
            self._draw_scene()
            self.clock.tick(60)

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.state.change_speed(1.5)
                if event.key == pygame.K_DOWN:
                    self.state.change_speed(1 / 1.5)
                if event.key == pygame.K_SPACE:
                    self.state.toggle_pause()
                if event.key == pygame.K_TAB:
                    self.current_view = 'back' if self.current_view == 'front' else 'front'
                    self._update_caption()

    def _update_caption(self):
        if self.current_view == 'front':
            pygame.display.set_caption("Ancient Antikythera - Geocentric View")
        else:
            pygame.display.set_caption("Ancient Antikythera - Back Dials")

    def _draw_scene(self):
        if self.current_view == 'front':
            self.front_renderer.draw_background()
            self.front_renderer.draw_front_dials(self.state.current_day)
            self.front_renderer.draw_celestial_bodies(self.state.body_angles)
            self.front_renderer.draw_moon_phase(self.state.body_angles['Sun'], self.state.body_angles['Moon'])
            self.front_renderer.draw_ui(self.state.current_day, self.state.time_multiplier)
        else: # Back view
            self.back_renderer.draw_background()
            self.back_renderer.draw_metonic_dial(self.state.current_day)
            self.back_renderer.draw_saros_dial(self.state.current_day)
            self.back_renderer.draw_games_dial(self.state.current_day)
            self.back_renderer.draw_exeligmos_dial(self.state.current_day)
            self.back_renderer.draw_legend()
            self.back_renderer.draw_ui(self.state.current_day, self.state.time_multiplier)
        pygame.display.flip()

if __name__ == "__main__":
    app = AncientAntikythera()
    app.run()
