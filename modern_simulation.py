"""
Simulation state and main loop for the Modern Antikythera simulation.
This file manages the simulation's state, including the current date,
time multiplier, and planet angles. It also contains the main application loop.
"""
import pygame
import sys
import math
from datetime import datetime, timedelta
import modern_config as config
import modern_drawing as drawing
from modern_back_face import ModernBackRenderer

class SimulationState:
    """Manages the state of the simulation."""
    def __init__(self, width):
        self.current_date = datetime.now()
        self.time_multiplier = 1.0
        self.paused = False
        self.planet_angles = {name: math.radians(i * 45) for i, name in enumerate(config.PLANET_VISUAL_DATA)}

        self.fonts = {
            'small': pygame.font.SysFont('Arial', int(width / 85)),
            'medium': pygame.font.SysFont('Arial', int(width / 67)),
            'large': pygame.font.SysFont('Arial', int(width / 50), bold=True),
            'planet': pygame.font.SysFont('Arial', int(width / 75)),
            'zodiac': pygame.font.SysFont('Arial', int(width / 60)),
            'day': pygame.font.SysFont('Arial', int(width / 100)),
            'parapegma': pygame.font.SysFont('Arial', int(width / 65), bold=True)
        }

    def update(self, delta_time):
        """Updates the simulation state."""
        if not self.paused:
            self.current_date += timedelta(days=self.time_multiplier * delta_time)
            for name, data in config.PLANET_VISUAL_DATA.items():
                angle_change = math.radians(data['speed'] * self.time_multiplier * delta_time)
                self.planet_angles[name] += angle_change

class ModernAntikythera:
    """Main application class."""
    def __init__(self):
        pygame.init()
        info = pygame.display.Info()
        screen_height = info.current_h
        self.WIDTH = self.HEIGHT = min(1200, screen_height - 80)
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Modern Antikythera")

        self.simulation_state = SimulationState(self.WIDTH)
        self.front_renderer = drawing
        self.back_renderer = ModernBackRenderer(self.screen, self.simulation_state.fonts)
        self.current_view = 'front'

    def run(self):
        """Main application loop."""
        clock = pygame.time.Clock()
        running = True
        while running:
            delta_time = clock.tick(60) / 1000.0 * 60 # Normalize to 60 FPS

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.simulation_state.time_multiplier *= 1.5
                    if event.key == pygame.K_DOWN:
                        self.simulation_state.time_multiplier /= 1.5
                    if event.key == pygame.K_SPACE:
                        self.simulation_state.paused = not self.simulation_state.paused
                    if event.key == pygame.K_TAB:
                        self.current_view = 'back' if self.current_view == 'front' else 'front'
                        self._update_caption()

            self.simulation_state.update(delta_time)
            self._draw_scene()
            pygame.display.flip()

        pygame.quit()
        sys.exit()

    def _update_caption(self):
        if self.current_view == 'front':
            pygame.display.set_caption("Modern Antikythera - Solar System View")
        else:
            pygame.display.set_caption("Modern Antikythera - Astronomical Cycles")

    def _draw_scene(self):
        if self.current_view == 'front':
            self.front_renderer.draw_gradient_background(self.screen)
            self.front_renderer.draw_celestial_bodies(self.screen, self.simulation_state)
            self.front_renderer.draw_calendar_and_zodiac_dials(self.screen, self.simulation_state)
            self.front_renderer.draw_large_moon_phase(self.screen, self.simulation_state, self.simulation_state.fonts)
            self.front_renderer.draw_parapegma_legend(self.screen, self.simulation_state.fonts)
            self.front_renderer.draw_ui(self.screen, self.simulation_state)
        else: # Back view
            self.back_renderer.draw_background()
            self.back_renderer.draw_metonic_dial(self.simulation_state)
            self.back_renderer.draw_saros_dial(self.simulation_state)
            self.back_renderer.draw_games_dial(self.simulation_state)
            self.back_renderer.draw_exeligmos_dial(self.simulation_state)
            self.back_renderer.draw_legend()
            self.back_renderer.draw_ui(self.simulation_state)

if __name__ == '__main__':
    app = ModernAntikythera()
    app.run()
