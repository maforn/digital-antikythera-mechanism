"""
Drawing functions for the Modern Antikythera simulation.
This file contains functions for rendering all visual elements of the simulation,
including the background, celestial bodies, dials, and UI components.
"""
import pygame
import math
from datetime import datetime
import modern_config as config

def draw_gradient_background(surface):
    """Draws a vertical gradient background."""
    height = surface.get_height()
    for y in range(height):
        ratio = y / height
        r = int(config.BG_COLOR_TOP[0] * (1 - ratio) + config.BG_COLOR_BOTTOM[0] * ratio)
        g = int(config.BG_COLOR_TOP[1] * (1 - ratio) + config.BG_COLOR_BOTTOM[1] * ratio)
        b = int(config.BG_COLOR_TOP[2] * (1 - ratio) + config.BG_COLOR_BOTTOM[2] * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (surface.get_width(), y))

def draw_glowing_circle(surface, color, center, radius):
    """Draws a circle with a glowing effect."""
    pygame.draw.circle(surface, color, center, radius)
    if radius > 2:
        glow_surface = pygame.Surface((radius * 4, radius * 4), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, (*color, 30), (radius * 2, radius * 2), radius * 2)
        pygame.draw.circle(glow_surface, (*color, 50), (radius * 2, radius * 2), int(radius * 1.5))
        surface.blit(glow_surface, (center[0] - radius * 2, center[1] - radius * 2))

def draw_small_orbiting_moon(surface, earth_center, earth_radius, simulation_state):
    """Draws the small moon orbiting Earth."""
    moon_size = max(1, int(earth_radius / 2.5))
    moon_orbit_radius = earth_radius + max(5, int(earth_radius * 1.5))

    days_into_cycle = (simulation_state.current_date - datetime.strptime(config.MOON_EPOCH, "%Y-%m-%d")).total_seconds() / (24 * 3600)
    phase = (days_into_cycle / config.SYNODIC_PERIOD) % 1.0

    earth_angle_to_sun = simulation_state.planet_angles['Earth']
    moon_phase_angle = phase * 2 * math.pi
    earth_moon_angle = earth_angle_to_sun + moon_phase_angle + math.pi

    moon_x = earth_center[0] + moon_orbit_radius * math.cos(earth_moon_angle)
    moon_y = earth_center[1] + moon_orbit_radius * math.sin(earth_moon_angle)
    moon_pos = (int(moon_x), int(moon_y))

    pygame.draw.circle(surface, (200, 200, 200), moon_pos, moon_size)
    pygame.draw.line(surface, (70, 70, 70), earth_center, moon_pos, 1)

def draw_large_moon_phase(surface, simulation_state, fonts):
    """Draws the large moon phase display."""
    width = surface.get_width()
    moon_radius = int(width / 15)
    moon_display_center = (width - moon_radius - 30, moon_radius + 30)

    pygame.draw.circle(surface, (20, 20, 30), moon_display_center, moon_radius + 10)

    days_into_cycle = (simulation_state.current_date - datetime.strptime(config.MOON_EPOCH, "%Y-%m-%d")).total_seconds() / (24 * 3600)
    phase = (days_into_cycle / config.SYNODIC_PERIOD) % 1.0

    moon_color_lit = (200, 200, 200)
    moon_color_dark = (80, 80, 80)

    pygame.draw.circle(surface, moon_color_dark, moon_display_center, moon_radius)

    lit_radius = 0
    if phase < 0.5:
        lit_radius = (phase / 0.5) * moon_radius
    else:
        lit_radius = (1 - (phase - 0.5) / 0.5) * moon_radius

    if lit_radius > 0:
        pygame.draw.circle(surface, moon_color_lit, moon_display_center, int(lit_radius))

    pygame.draw.circle(surface, (128, 128, 128), moon_display_center, moon_radius, 1)

    phase_index = int((phase * 8 + 0.5)) % 8
    current_phase_name = config.MOON_PHASE_NAMES[phase_index]
    phase_text_surface = fonts['medium'].render(f"Moon: {current_phase_name}", True, (255, 255, 255))
    surface.blit(phase_text_surface, (
        moon_display_center[0] - phase_text_surface.get_width() // 2,
        moon_display_center[1] + moon_radius + 15
    ))

def draw_celestial_bodies(surface, simulation_state):
    """Draws the Sun and all planets."""
    width = surface.get_width()
    center = (width // 2, width // 2)
    sun_radius = int(width / 48)
    draw_glowing_circle(surface, (255, 180, 0), center, sun_radius)

    orbit_spacing = int(width / 26.6)
    base_orbit = int(width / 17)

    for i, (name, data) in enumerate(config.PLANET_VISUAL_DATA.items()):
        orbit_radius = base_orbit + i * orbit_spacing
        angle = simulation_state.planet_angles[name]
        x = center[0] + orbit_radius * math.cos(angle)
        y = center[1] + orbit_radius * math.sin(angle)
        current_planet_pos = (int(x), int(y))
        planet_size = int(data['size'] * (width / 1200))

        pygame.draw.circle(surface, (80, 80, 100), center, orbit_radius, 1)
        draw_glowing_circle(surface, data['color'], current_planet_pos, planet_size)

        label_surface = simulation_state.fonts['planet'].render(name, True, data['color'])
        label_x = x + (planet_size + 10) * math.cos(angle)
        label_y = y + (planet_size + 10) * math.sin(angle)
        surface.blit(label_surface, label_surface.get_rect(center=(label_x, label_y)))

        if name == 'Earth':
            draw_small_orbiting_moon(surface, current_planet_pos, planet_size, simulation_state)

def draw_calendar_and_zodiac_dials(surface, simulation_state):
    """Draws the calendar, zodiac, and parapegma dials and the date pointer."""
    width = surface.get_width()
    center = (width // 2, width // 2)

    parapegma_radius = width // 2 - int(width / 30)
    zodiac_radius = parapegma_radius - int(width / 20)
    day_ring_radius = zodiac_radius - int(width / 25)
    month_radius = day_ring_radius - int(width / 25)

    # Draw Zodiac Ring
    angle_step_zodiac = 30
    for i, sign_name in enumerate(config.ZODIAC_INSCRIPTIONS):
        angle = math.radians(i * angle_step_zodiac - 90 + (angle_step_zodiac / 2))
        text_x = center[0] + (zodiac_radius - int(width / 60)) * math.cos(angle)
        text_y = center[1] + (zodiac_radius - int(width / 60)) * math.sin(angle)
        text_surface = simulation_state.fonts['zodiac'].render(sign_name, True, (180, 180, 220))
        surface.blit(text_surface, text_surface.get_rect(center=(text_x, text_y)))
        tick_angle = math.radians(i * angle_step_zodiac - 90)
        start_pos = (center[0] + (zodiac_radius - 10) * math.cos(tick_angle),
                     center[1] + (zodiac_radius - 10) * math.sin(tick_angle))
        end_pos = (center[0] + zodiac_radius * math.cos(tick_angle),
                   center[1] + zodiac_radius * math.sin(tick_angle))
        pygame.draw.line(surface, (100, 100, 120), start_pos, end_pos, 2)

    # Draw Day Ring
    for day in range(1, 366):
        angle = math.radians((day / 365.25) * 360 - 90)
        tick_length = 5 if day % 5 == 0 else 2
        start_pos = (center[0] + (day_ring_radius - tick_length) * math.cos(angle),
                     center[1] + (day_ring_radius - tick_length) * math.sin(angle))
        end_pos = (
            center[0] + day_ring_radius * math.cos(angle), center[1] + day_ring_radius * math.sin(angle))
        pygame.draw.line(surface, (120, 120, 120), start_pos, end_pos, 1)

        if day % 10 == 0:
            text_x = center[0] + (day_ring_radius - 15) * math.cos(angle)
            text_y = center[1] + (day_ring_radius - 15) * math.sin(angle)
            text_surface = simulation_state.fonts['day'].render(str(day), True, (150, 150, 150))
            text_surface = pygame.transform.rotate(text_surface, -math.degrees(angle) - 90)
            surface.blit(text_surface, text_surface.get_rect(center=(text_x, text_y)))

    # Draw Month Ring
    angle_step_month = 30
    for i, month_name in enumerate(config.MONTHS):
        angle = math.radians(i * angle_step_month - 90 + (angle_step_month / 2))
        text_x = center[0] + (month_radius - int(width / 60)) * math.cos(angle)
        text_y = center[1] + (month_radius - int(width / 60)) * math.sin(angle)
        text_surface = simulation_state.fonts['small'].render(month_name, True, (150, 150, 150))
        surface.blit(text_surface, text_surface.get_rect(center=(text_x, text_y)))

    # Draw Parapegma Markers
    for event, data in config.PARAPEGMA_MARKERS.items():
        day_of_year = data['day']
        symbol = data['symbol']
        angle = math.radians((day_of_year / 365.25) * 360 - 90)
        marker_x = int(center[0] + (parapegma_radius - int(width / 60)) * math.cos(angle))
        marker_y = int(center[1] + (parapegma_radius - int(width / 60)) * math.sin(angle))
        symbol_surface = simulation_state.fonts['parapegma'].render(symbol, True, (255, 223, 0))
        surface.blit(symbol_surface, symbol_surface.get_rect(center=(marker_x, marker_y)))

    # Draw Date Pointer
    day_of_year = simulation_state.current_date.timetuple().tm_yday
    date_angle = math.radians((day_of_year / 365.25) * 360 - 90)
    pointer_start_radius = month_radius - int(width / 34)
    pointer_end_radius = parapegma_radius
    start_x = center[0] + pointer_start_radius * math.cos(date_angle)
    start_y = center[1] + pointer_start_radius * math.sin(date_angle)
    end_x = center[0] + pointer_end_radius * math.cos(date_angle)
    end_y = center[1] + pointer_end_radius * math.sin(date_angle)
    pygame.draw.line(surface, (255, 100, 100), (start_x, start_y), (end_x, end_y), 2)
    pygame.draw.circle(surface, (255, 100, 100), (int(end_x), int(end_y)), 4)

def draw_parapegma_legend(surface, fonts):
    """Draws the legend for the parapegma symbols."""
    width = surface.get_width()
    height = surface.get_height()
    legend_x = 20
    legend_y = height - int(height / 7)
    legend_width = int(width / 5.5)
    legend_height = int(height / 8)

    legend_surface = pygame.Surface((legend_width, legend_height), pygame.SRCALPHA)
    legend_surface.fill((30, 30, 50, 180))
    surface.blit(legend_surface, (legend_x, legend_y))

    title_surface = fonts['medium'].render("Parapegma", True, (255, 255, 255))
    surface.blit(title_surface, (legend_x + 10, legend_y + 5))

    y_offset = 30
    for event, data in config.PARAPEGMA_MARKERS.items():
        if legend_y + y_offset > height - 20: break
        symbol_surface = fonts['medium'].render(f"{data['symbol']}:", True, (255, 223, 0))
        text_surface = fonts['small'].render(event, True, (200, 200, 200))
        surface.blit(symbol_surface, (legend_x + 15, legend_y + y_offset))
        surface.blit(text_surface, (legend_x + 55, legend_y + y_offset + 2))
        y_offset += int(height / 60)

def draw_ui(surface, simulation_state):
    """Draws the main UI elements like date and controls."""
    date_text = simulation_state.current_date.strftime("%Y - %b - %d")
    date_surface = simulation_state.fonts['large'].render(f"{date_text}", True, (255, 255, 255))
    surface.blit(date_surface, (10, 10))

    controls = ["Controls:", "UP/DOWN: Change Speed", "SPACE: Pause/Resume", f"Speed: {simulation_state.time_multiplier:.2f}x"]
    for i, line in enumerate(controls):
        text_surface = simulation_state.fonts['medium'].render(line, True, (200, 200, 200))
        surface.blit(text_surface, (10, 50 + i * 25))

