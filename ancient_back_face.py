"""
Drawing module for the back face of the Ancient Antikythera Simulation.
This file contains the AncientBackRenderer class, which handles all drawing operations
for the back dials of the mechanism, including the Metonic, Saros, Games, and Exeligmos dials.
"""
import pygame
import math
import ancient_config as config


class AncientBackRenderer:
    """Handles all rendering for the back face of the ancient simulation."""

    def __init__(self, screen, fonts):
        self.screen = screen
        self.fonts = fonts
        self.WIDTH, self.HEIGHT = screen.get_size()
        # Adjust centers for upper and lower dials
        self.UPPER_CENTER = (self.WIDTH // 2, int(self.HEIGHT * 0.35))
        self.LOWER_CENTER = (self.WIDTH // 2, int(self.HEIGHT * 0.75))

    def draw_background(self):
        self.screen.fill(config.BG_COLOR)

    def _get_spiral_point(self, center, angle, distance_from_center):
        x = center[0] + math.cos(angle) * distance_from_center
        y = center[1] + math.sin(angle) * distance_from_center
        return (x, y)

    def draw_metonic_dial(self, current_day):
        """Draws the upper Metonic spiral dial."""
        dial_radius = self.HEIGHT / 4
        total_months = 235
        months_per_loop = 47  # 235 / 5 loops
        spiral_loops = 5

        # Draw the spiral path
        points = []
        for i in range(total_months * 4):  # 4 points per month for smoothness
            angle = math.radians(i * (360 / (months_per_loop * 4)) - 90)
            t = i / (total_months * 4)
            radius = dial_radius - (t * dial_radius * 0.95)
            point = self._get_spiral_point(self.UPPER_CENTER, angle, radius)
            points.append(point)
        if len(points) > 1:
            pygame.draw.lines(self.screen, config.DIAL_COLOR, False, points, 2)

        # Draw month markings and labels
        for month_idx in range(total_months):
            angle = math.radians(month_idx * (360 / months_per_loop) - 90)
            t = month_idx / total_months
            radius = dial_radius - (t * dial_radius * 0.95)

            mark_length = 10
            start_point = self._get_spiral_point(self.UPPER_CENTER, angle, radius - mark_length / 2)
            end_point = self._get_spiral_point(self.UPPER_CENTER, angle, radius + mark_length / 2)
            pygame.draw.line(self.screen, config.DIAL_COLOR, start_point, end_point, 1)

            # Draw month labels (simplified)
            if month_idx % 12 == 0:  # Label every 12th month
                label_angle = math.radians(month_idx * (360 / months_per_loop) - 90)
                label_radius = radius + 15
                label_pos = self._get_spiral_point(self.UPPER_CENTER, label_angle, label_radius)

                month_name = config.METONIC_MONTHS[month_idx % 12]
                text_surface = self.fonts['small'].render(month_name, True, config.TEXT_COLOR)
                text_rect = text_surface.get_rect(center=label_pos)
                self.screen.blit(text_surface, text_rect)

        # Draw pointer
        synodic_month_days = 29.530589
        current_month = (current_day / synodic_month_days) % total_months

        pointer_angle = math.radians(current_month * (360 / months_per_loop) - 90)
        pointer_t = current_month / total_months
        pointer_radius = dial_radius - (pointer_t * dial_radius * 0.95)

        end_point = self._get_spiral_point(self.UPPER_CENTER, pointer_angle, pointer_radius)
        pygame.draw.line(self.screen, config.POINTER_COLOR, self.UPPER_CENTER, end_point, 2)
        pygame.draw.circle(self.screen, config.POINTER_COLOR, (int(end_point[0]), int(end_point[1])), 5)
        pygame.draw.circle(self.screen, config.DIAL_COLOR, self.UPPER_CENTER, 8)

    def draw_saros_dial(self, current_day):
        """Draws the lower Saros spiral dial for eclipse prediction."""
        dial_radius = self.HEIGHT / 4.5
        total_months = 223
        months_per_loop = 55.75  # 223 / 4 loops

        # Draw the spiral path (4 loops)
        points = []
        for i in range(total_months * 4):  # 4 points per month for smoothness
            angle = math.radians(i * (360 / (months_per_loop * 4)) - 90)
            t = i / (total_months * 4)
            radius = dial_radius - (t * dial_radius * 0.9)
            point = self._get_spiral_point(self.LOWER_CENTER, angle, radius)
            points.append(point)
        if len(points) > 1:
            pygame.draw.lines(self.screen, config.DIAL_COLOR, False, points, 2)

        # Draw month markings and eclipse glyphs (simplified)
        # In a real reconstruction, these would be based on complex astronomical data.
        # Here, we'll just mark a few for visual effect.
        for month_idx in range(total_months):
            angle = math.radians(month_idx * (360 / months_per_loop) - 90)
            t = month_idx / total_months
            radius = dial_radius - (t * dial_radius * 0.9)

            start_point = self._get_spiral_point(self.LOWER_CENTER, angle, radius - 3)
            end_point = self._get_spiral_point(self.LOWER_CENTER, angle, radius + 3)
            pygame.draw.line(self.screen, config.DIAL_COLOR, start_point, end_point, 1)

            # Example eclipse glyphs
            if month_idx in [18, 41, 72, 110, 155, 200]:
                glyph_pos = self._get_spiral_point(self.LOWER_CENTER, angle, radius + 10)
                glyph = "Σ" if month_idx % 2 == 0 else "Η"  # Sigma for Lunar, Eta for Solar
                text_surface = self.fonts['small'].render(glyph, True, (255, 100, 100))
                text_rect = text_surface.get_rect(center=glyph_pos)
                self.screen.blit(text_surface, text_rect)

        # Draw pointer
        synodic_month_days = 29.530589
        current_month_in_saros = (current_day / synodic_month_days) % total_months

        pointer_angle = math.radians(current_month_in_saros * (360 / months_per_loop) - 90)
        pointer_t = current_month_in_saros / total_months
        pointer_radius = dial_radius - (pointer_t * dial_radius * 0.9)

        end_point = self._get_spiral_point(self.LOWER_CENTER, pointer_angle, pointer_radius)
        pygame.draw.line(self.screen, config.POINTER_COLOR, self.LOWER_CENTER, end_point, 2)
        pygame.draw.circle(self.screen, config.POINTER_COLOR, (int(end_point[0]), int(end_point[1])), 4)
        pygame.draw.circle(self.screen, config.DIAL_COLOR, self.LOWER_CENTER, 8)

    def draw_games_dial(self, current_day):
        """Draws the small Games dial."""
        dial_radius = self.HEIGHT / 16
        dial_center = (self.WIDTH * 0.85, self.HEIGHT * 0.25)  # Positioned on the top right

        pygame.draw.circle(self.screen, config.DIAL_COLOR, dial_center, dial_radius, 1)

        # Draw the 4 sectors
        for i in range(4):
            angle = math.radians(i * 90 - 45)
            end_angle = math.radians((i + 1) * 90 - 45)

            # Draw sector lines
            start_pos = self._get_spiral_point(dial_center, angle, 0)
            end_pos = self._get_spiral_point(dial_center, angle, dial_radius)
            pygame.draw.line(self.screen, config.DIAL_COLOR, dial_center, end_pos, 1)

            # Draw labels
            game1, game2 = config.GAMES_INSCRIPTIONS[i + 1]

            label_angle = math.radians(i * 90)
            text_pos1 = self._get_spiral_point(dial_center, label_angle, dial_radius * 0.6)
            text_surface1 = self.fonts['small'].render(game1[:4], True, config.TEXT_COLOR)
            self.screen.blit(text_surface1, text_surface1.get_rect(center=text_pos1))

        # Draw pointer
        year_in_cycle = int((current_day / 365.25) % 4)
        pointer_angle = math.radians(year_in_cycle * 90)

        end_point = self._get_spiral_point(dial_center, pointer_angle, dial_radius)
        pygame.draw.line(self.screen, config.POINTER_COLOR, dial_center, end_point, 2)

    def draw_exeligmos_dial(self, current_day):
        """Draws the small Exeligmos dial."""
        dial_radius = self.HEIGHT / 16
        dial_center = (self.WIDTH * 0.85, self.HEIGHT * 0.75)  # Positioned on the bottom right

        pygame.draw.circle(self.screen, config.DIAL_COLOR, dial_center, dial_radius, 1)

        # Draw the 3 sectors
        for i in range(3):
            angle = math.radians(i * 120 - 30)

            # Draw sector lines
            end_pos = self._get_spiral_point(dial_center, angle, dial_radius)
            pygame.draw.line(self.screen, config.DIAL_COLOR, dial_center, end_pos, 1)

            # Draw labels
            label_angle = math.radians(i * 120 + 30)
            label_pos = self._get_spiral_point(dial_center, label_angle, dial_radius * 0.7)
            text_surface = self.fonts['medium'].render(config.EXELIGMOS_LABELS[i], True, config.TEXT_COLOR)
            self.screen.blit(text_surface, text_surface.get_rect(center=label_pos))

        # Draw pointer
        saros_cycle_days = 6585.3211
        exeligmos_period_in_saros = 3
        current_saros_cycle = (current_day / saros_cycle_days)
        exeligmos_segment = int(current_saros_cycle % exeligmos_period_in_saros)

        pointer_angle = math.radians(exeligmos_segment * 120 + 30)
        end_point = self._get_spiral_point(dial_center, pointer_angle, dial_radius)
        pygame.draw.line(self.screen, config.POINTER_COLOR, dial_center, end_point, 2)

    def draw_legend(self):
        """Draws a legend explaining the dials."""
        legend_x = 20
        legend_y = self.HEIGHT - 140
        line_height = 22

        legend_items = [
            ("Metonic Dial:", "19-year calendar cycle"),
            ("Saros Dial:", "18-year eclipse prediction cycle"),
            ("Games Dial:", "4-year Panhellenic games cycle"),
            ("Exeligmos Dial:", "54-year eclipse timing correction")
        ]

        title_surface = self.fonts['medium'].render("Back Face Dials", True, config.TEXT_COLOR)
        self.screen.blit(title_surface, (legend_x, legend_y))

        for i, (title, desc) in enumerate(legend_items):
            y_pos = legend_y + (i + 1) * line_height
            title_surf = self.fonts['small'].render(title, True, config.POINTER_COLOR)
            desc_surf = self.fonts['small'].render(desc, True, config.TEXT_COLOR)
            self.screen.blit(title_surf, (legend_x, y_pos))
            self.screen.blit(desc_surf, (legend_x + title_surf.get_width() + 5, y_pos))

    def draw_ui(self, current_day, time_multiplier):
        day_text = f"Day: {int(current_day)}"
        day_surface = self.fonts['large'].render(day_text, True, config.TEXT_COLOR)
        self.screen.blit(day_surface, (10, 10))

        controls = ["Controls:", "UP/DOWN: Change Speed", "SPACE: Pause/Resume", "TAB: Switch View",
                    f"Speed: {time_multiplier:.2f}x"]
        for i, line in enumerate(controls):
            text_surface = self.fonts['medium'].render(line, True, config.TEXT_COLOR)
            self.screen.blit(text_surface, (10, 50 + i * 25))
