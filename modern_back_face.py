"""
Drawing module for the back face of the Modern Antikythera Simulation.
This file contains the ModernBackRenderer class, which handles all drawing operations
for the back dials with a modern aesthetic.
"""
import pygame
import math
from datetime import datetime
import modern_config as config

class ModernBackRenderer:
    """Handles all rendering for the back face of the modern simulation."""
    def __init__(self, screen, fonts):
        self.screen = screen
        self.fonts = fonts
        self.WIDTH, self.HEIGHT = screen.get_size()
        self.CENTER = (self.WIDTH // 2, self.HEIGHT // 2)

        # Define positions for the dials
        self.metonic_pos = (self.WIDTH * 0.3, self.HEIGHT * 0.35)
        self.saros_pos = (self.WIDTH * 0.7, self.HEIGHT * 0.35)
        self.games_pos = (self.WIDTH * 0.3, self.HEIGHT * 0.75)
        self.exeligmos_pos = (self.WIDTH * 0.7, self.HEIGHT * 0.75)

    def draw_background(self):
        """Draws a modern, clean background."""
        self.screen.fill((10, 15, 30))

    def _draw_dial_base(self, center, radius, title):
        """Helper to draw the base of a dial."""
        pygame.draw.circle(self.screen, config.DIAL_BG_COLOR, center, radius)
        pygame.draw.circle(self.screen, config.DIAL_OUTLINE_COLOR, center, radius, 2)

        title_surface = self.fonts['medium'].render(title, True, config.BACK_TEXT_COLOR)
        self.screen.blit(title_surface, title_surface.get_rect(center=(center[0], center[1] - radius - 20)))

    def _draw_progress_arc(self, center, radius, progress):
        """Helper to draw a circular progress bar."""
        if progress <= 0: return
        rect = pygame.Rect(center[0] - radius, center[1] - radius, radius * 2, radius * 2)

        # Background
        pygame.draw.arc(self.screen, config.PROGRESS_BG_COLOR, rect, -math.pi/2, 2 * math.pi - math.pi/2, 8)

        # Foreground
        end_angle = -math.pi/2 + (progress * 2 * math.pi)
        pygame.draw.arc(self.screen, config.PROGRESS_BAR_COLOR, rect, -math.pi/2, end_angle, 8)

    def draw_metonic_dial(self, simulation_state):
        """Draws the Metonic cycle dial."""
        radius = self.WIDTH / 8
        self._draw_dial_base(self.metonic_pos, radius, "Metonic Cycle")

        total_days = config.METONIC_CYCLE_YEARS * 365.25
        days_in_cycle = (simulation_state.current_date - datetime(2000, 1, 1)).total_seconds() / (24 * 3600)
        progress = (days_in_cycle % total_days) / total_days

        self._draw_progress_arc(self.metonic_pos, radius - 20, progress)

        year_in_cycle = int(days_in_cycle / 365.25) % config.METONIC_CYCLE_YEARS + 1
        text = f"Year {year_in_cycle} / {config.METONIC_CYCLE_YEARS}"
        surface = self.fonts['medium'].render(text, True, config.BACK_TEXT_COLOR)
        self.screen.blit(surface, surface.get_rect(center=self.metonic_pos))

    def draw_saros_dial(self, simulation_state):
        """Draws the Saros eclipse cycle dial."""
        radius = self.WIDTH / 8
        self._draw_dial_base(self.saros_pos, radius, "Saros Cycle")

        total_days = config.SAROS_CYCLE_YEARS * 365.25
        days_in_cycle = (simulation_state.current_date - datetime(2000, 1, 1)).total_seconds() / (24 * 3600)
        progress = (days_in_cycle % total_days) / total_days

        self._draw_progress_arc(self.saros_pos, radius - 20, progress)

        month_in_cycle = int((days_in_cycle / config.SYNODIC_PERIOD) % config.SAROS_CYCLE_MONTHS)
        text = f"Month {month_in_cycle} / {config.SAROS_CYCLE_MONTHS}"
        surface = self.fonts['medium'].render(text, True, config.BACK_TEXT_COLOR)
        self.screen.blit(surface, surface.get_rect(center=self.saros_pos))

    def draw_games_dial(self, simulation_state):
        """Draws the modern 'Games' dial."""
        radius = self.WIDTH / 8
        self._draw_dial_base(self.games_pos, radius, "Global Events")

        year_in_cycle = simulation_state.current_date.year % 4
        game_name = config.MODERN_GAMES[year_in_cycle]

        text_surface = self.fonts['medium'].render(game_name, True, config.BACK_TEXT_COLOR)
        self.screen.blit(text_surface, text_surface.get_rect(center=self.games_pos))

        progress = (simulation_state.current_date.timetuple().tm_yday / 365)
        self._draw_progress_arc(self.games_pos, radius - 20, progress)

    def draw_exeligmos_dial(self, simulation_state):
        """Draws the Exeligmos cycle dial."""
        radius = self.WIDTH / 8
        self._draw_dial_base(self.exeligmos_pos, radius, "Exeligmos Cycle")

        total_days = config.EXELIGMOS_CYCLE_YEARS * 365.25
        days_in_cycle = (simulation_state.current_date - datetime(2000, 1, 1)).total_seconds() / (24 * 3600)
        progress = (days_in_cycle % total_days) / total_days

        self._draw_progress_arc(self.exeligmos_pos, radius - 20, progress)

        saros_in_cycle = int((days_in_cycle / (config.SAROS_CYCLE_YEARS * 365.25)) % config.EXELIGMOS_CYCLE_SAROS) + 1
        text = f"Saros {saros_in_cycle} / {config.EXELIGMOS_CYCLE_SAROS}"
        surface = self.fonts['medium'].render(text, True, config.BACK_TEXT_COLOR)
        self.screen.blit(surface, surface.get_rect(center=self.exeligmos_pos))

    def draw_legend(self):
        """Draws a legend for the modern back face."""
        legend_x = 20
        legend_y = self.HEIGHT - 120
        line_height = 25

        legend_items = [
            ("Metonic Cycle:", "19-year calendar cycle for aligning solar and lunar years."),
            ("Saros Cycle:", "18-year cycle for predicting eclipses."),
            ("Global Events:", "Tracks major international quadrennial events."),
            ("Exeligmos Cycle:", "54-year cycle for more precise eclipse timing.")
        ]

        title_surface = self.fonts['medium'].render("Back Dials Explained", True, config.BACK_TEXT_COLOR)
        self.screen.blit(title_surface, (legend_x, legend_y))

        for i, (title, desc) in enumerate(legend_items):
            y_pos = legend_y + (i + 1) * line_height
            title_surf = self.fonts['small'].render(title, True, config.PROGRESS_BAR_COLOR)
            desc_surf = self.fonts['small'].render(desc, True, config.BACK_TEXT_COLOR)
            self.screen.blit(title_surf, (legend_x, y_pos))
            self.screen.blit(desc_surf, (legend_x + title_surf.get_width() + 10, y_pos))

    def draw_ui(self, simulation_state):
        """Draws the main UI elements."""
        date_text = simulation_state.current_date.strftime("%Y - %b - %d")
        date_surface = self.fonts['large'].render(f"{date_text}", True, config.BACK_TEXT_COLOR)
        self.screen.blit(date_surface, (10, 10))

        controls = ["Controls:", "UP/DOWN: Speed", "SPACE: Pause", "TAB: Switch View", f"Speed: {simulation_state.time_multiplier:.2f}x"]
        for i, line in enumerate(controls):
            text_surface = self.fonts['medium'].render(line, True, config.BACK_TEXT_COLOR)
            self.screen.blit(text_surface, (10, 50 + i * 25))
