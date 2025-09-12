"""
Drawing module for the Ancient Antikythera Simulation.
This file contains the AncientRenderer class, which handles all drawing operations
for a geocentric model based on the historical mechanism.
"""
import pygame
import math
from datetime import datetime
import ancient_config as config

class AncientRenderer:
    """Handles all rendering for the ancient simulation."""
    def __init__(self, screen, fonts):
        self.screen = screen
        self.fonts = fonts
        self.WIDTH, self.HEIGHT = screen.get_size()
        self.CENTER = (self.WIDTH // 2, self.HEIGHT // 2)

    def draw_background(self):
        self.screen.fill(config.BG_COLOR)

    def draw_celestial_bodies(self, body_angles):
        # Draw central Earth
        pygame.draw.circle(self.screen, (0, 150, 255), self.CENTER, 15)

        # Normalize distances to prevent clipping
        max_dist_raw = max(d['distance'] for d in config.GEOCENTRIC_DATA.values())
        max_screen_dist = self.WIDTH // 2 - 80 # Add some padding

        for name, data in config.GEOCENTRIC_DATA.items():
            normalized_dist = data['distance'] / max_dist_raw
            orbit_radius = int(max_screen_dist * normalized_dist)
            angle = body_angles[name]
            x = self.CENTER[0] + orbit_radius * math.cos(angle)
            y = self.CENTER[1] + orbit_radius * math.sin(angle)

            pygame.draw.circle(self.screen, (*data['color'], 50), self.CENTER, orbit_radius, 1)
            pygame.draw.line(self.screen, (*data['color'], 80), self.CENTER, (x, y), 1)
            pygame.draw.circle(self.screen, data['color'], (int(x), int(y)), data['size'])

            label_surface = self.fonts['planet'].render(name, True, data['color'])
            label_x = x + (data['size'] + 10) * math.cos(angle)
            label_y = y + (data['size'] + 10) * math.sin(angle)
            self.screen.blit(label_surface, label_surface.get_rect(center=(label_x, label_y)))

    def draw_front_dials(self, current_day):
        zodiac_radius = int(self.WIDTH / 2.5)
        month_radius = zodiac_radius - int(self.WIDTH / 15)

        # Draw Zodiac Dial
        pygame.draw.circle(self.screen, config.DIAL_COLOR, self.CENTER, zodiac_radius, 2)
        for i in range(12):
            angle_deg = i * 30
            angle_rad = math.radians(angle_deg - 90)
            start_pos = (self.CENTER[0] + month_radius * math.cos(angle_rad), self.CENTER[1] + month_radius * math.sin(angle_rad))
            end_pos = (self.CENTER[0] + zodiac_radius * math.cos(angle_rad), self.CENTER[1] + zodiac_radius * math.sin(angle_rad))
            pygame.draw.line(self.screen, config.DIAL_COLOR, start_pos, end_pos, 2)

            label_angle_rad = math.radians(angle_deg - 15 - 90)
            text_surface = self.fonts['zodiac'].render(config.ZODIAC_INSCRIPTIONS_GREEK[i], True, config.TEXT_COLOR)
            text_rect = text_surface.get_rect(center=(
                self.CENTER[0] + (zodiac_radius - 20) * math.cos(label_angle_rad),
                self.CENTER[1] + (zodiac_radius - 20) * math.sin(label_angle_rad)
            ))
            self.screen.blit(text_surface, text_rect)

        # Draw Egyptian Calendar Dial (354-day)
        pygame.draw.circle(self.screen, config.DIAL_COLOR, self.CENTER, month_radius, 2)
        for i in range(354):
            angle = math.radians(i * (360 / 354))
            tick_len = 5 if i % 5 == 0 else 2
            start_pos = (self.CENTER[0] + (month_radius - tick_len) * math.cos(angle), self.CENTER[1] + (month_radius - tick_len) * math.sin(angle))
            end_pos = (self.CENTER[0] + month_radius * math.cos(angle), self.CENTER[1] + month_radius * math.sin(angle))
            pygame.draw.line(self.screen, config.TEXT_COLOR, start_pos, end_pos, 1)

        # Draw Egyptian Month Labels
        for i, month in enumerate(config.EGYPTIAN_MONTHS):
            angle_rad = math.radians(i * 30 - 15 - 90)
            text_surface = self.fonts['small'].render(month, True, config.TEXT_COLOR)
            text_rect = text_surface.get_rect(center=(
                self.CENTER[0] + (month_radius - 25) * math.cos(angle_rad),
                self.CENTER[1] + (month_radius - 25) * math.sin(angle_rad)
            ))
            self.screen.blit(text_surface, text_rect)

        # Draw Date Pointer for 354-day cycle
        date_angle = math.radians((current_day % 354 / 354) * 360 - 90)
        start_x = self.CENTER[0] + (month_radius - 40) * math.cos(date_angle)
        start_y = self.CENTER[1] + (month_radius - 40) * math.sin(date_angle)
        end_x = self.CENTER[0] + zodiac_radius * math.cos(date_angle)
        end_y = self.CENTER[1] + zodiac_radius * math.sin(date_angle)
        pygame.draw.line(self.screen, config.POINTER_COLOR, (start_x, start_y), (end_x, end_y), 2)
        pygame.draw.circle(self.screen, config.POINTER_COLOR, (int(end_x), int(end_y)), 4)

    def draw_moon_phase(self, sun_angle, moon_angle):
        """Draws the large moon phase display with a simple fill/shrink animation."""
        moon_radius = int(self.WIDTH / 15)
        moon_display_center = (self.WIDTH - moon_radius - 30, moon_radius + 30)

        # Background for the display
        pygame.draw.circle(self.screen, (20, 20, 30), moon_display_center, moon_radius + 10)

        # Calculate phase
        angle_diff = (moon_angle - sun_angle + math.pi) % (2 * math.pi)
        phase = angle_diff / (2 * math.pi)

        # Always draw the dark circle as a base
        pygame.draw.circle(self.screen, config.MOON_COLOR_DARK, moon_display_center, moon_radius)

        lit_radius = 0
        if phase < 0.5:  # Waxing (growing)
            # Radius grows from 0 to moon_radius
            lit_radius = (phase / 0.5) * moon_radius
        else:  # Waning (shrinking)
            # Radius shrinks from moon_radius to 0
            lit_radius = (1 - (phase - 0.5) / 0.5) * moon_radius

        if lit_radius > 0:
            pygame.draw.circle(self.screen, config.MOON_COLOR_LIT, moon_display_center, int(lit_radius))

        # Draw border
        pygame.draw.circle(self.screen, (128, 128, 128), moon_display_center, moon_radius, 1)

        # Label
        phase_index = int((phase * 8 + 0.5)) % 8
        current_phase_name = config.MOON_PHASE_NAMES[phase_index]
        phase_text_surface = self.fonts['medium'].render(f"Moon: {current_phase_name}", True, config.TEXT_COLOR)
        self.screen.blit(phase_text_surface, (
            moon_display_center[0] - phase_text_surface.get_width() // 2,
            moon_display_center[1] + moon_radius + 15
        ))

    def draw_ui(self, current_day, time_multiplier):
        day_text = f"Day: {int(current_day)}"
        day_surface = self.fonts['large'].render(day_text, True, config.TEXT_COLOR)
        self.screen.blit(day_surface, (10, 10))

        controls = ["Controls:", "UP/DOWN: Change Speed", "SPACE: Pause/Resume", f"Speed: {time_multiplier:.2f}x"]
        for i, line in enumerate(controls):
            text_surface = self.fonts['medium'].render(line, True, config.TEXT_COLOR)
            self.screen.blit(text_surface, (10, 50 + i * 25))
