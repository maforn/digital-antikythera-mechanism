import pygame
import numpy as np
import cv2
import os
from PIL import Image
from datetime import datetime
from modern_simulation import ModernAntikythera
import sys
import math


class SimulationRecorder:
    """Records the simulation to GIF and MP4 formats."""

    def __init__(self, app, output_dir="recordings"):
        self.app = app
        self.output_dir = output_dir
        self.recording = False
        self.frames = []
        self.video_writer = None
        os.makedirs(output_dir, exist_ok=True)

    def start_recording(self, view, speed_multiplier, duration_seconds=10, formats=['mp4']):
        """Start recording a specific view at a given speed."""
        if self.recording:
            print("Already recording!")
            return

        self.recording = True
        self.frames = []

        original_view = self.app.current_view
        original_speed = self.app.simulation_state.time_multiplier
        original_paused = self.app.simulation_state.paused

        self.app.current_view = view
        self.app.simulation_state.time_multiplier = speed_multiplier
        self.app.simulation_state.paused = False
        self.app._update_caption()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        speed_name = f"speed_{speed_multiplier:.2f}x".replace('.', '_')
        base_filename = f"antikythera_{view}_{speed_name}_{timestamp}"

        if 'mp4' in formats:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            mp4_path = os.path.join(self.output_dir, f"{base_filename}.mp4")
            self.video_writer = cv2.VideoWriter(mp4_path, fourcc, 60.0,
                                                (self.app.WIDTH, self.app.HEIGHT))

        print(f"Recording {view} view at {speed_multiplier:.2f}x speed for {duration_seconds:.2f} seconds...")

        clock = pygame.time.Clock()
        frames_to_record = int(duration_seconds * 60)  # 60 FPS

        for frame_num in range(frames_to_record):
            delta_time = clock.tick(60) / 1000.0 * 60
            self.app.simulation_state.update(delta_time)

            self.app._draw_scene()
            pygame.display.flip()

            frame_surface = pygame.display.get_surface()
            frame_array = pygame.surfarray.array3d(frame_surface)
            frame_array = np.rot90(frame_array)
            frame_array = np.flipud(frame_array)

            if 'gif' in formats:
                self.frames.append(frame_array.copy())

            if 'mp4' in formats and self.video_writer:
                frame_bgr = cv2.cvtColor(frame_array, cv2.COLOR_RGB2BGR)
                self.video_writer.write(frame_bgr)

            if (frame_num + 1) % 60 == 0:
                print(f"Recorded {(frame_num + 1) // 60} seconds...")

        if self.video_writer:
            self.video_writer.release()
            print(f"MP4 saved: {mp4_path}")

        if 'gif' in formats and self.frames:
            gif_path = os.path.join(self.output_dir, f"{base_filename}.gif")
            self._save_gif(gif_path)
            print(f"GIF saved: {gif_path}")

        self.app.current_view = original_view
        self.app.simulation_state.time_multiplier = original_speed
        self.app.simulation_state.paused = original_paused
        self.app._update_caption()

        self.recording = False
        self.frames = []
        print("Recording completed!")

    def _save_gif(self, filepath):
        """Save frames as GIF."""
        images = [Image.fromarray(frame) for frame in self.frames[::2]]
        images[0].save(
            filepath,
            save_all=True,
            append_images=images[1:],
            duration=33,  # ~30 FPS
            loop=0
        )


def add_recording_to_main_app():
    """Add recording functionality to the main ModernAntikythera class."""

    def __init_with_recorder__(self):
        self.__original_init__()
        self.recorder = SimulationRecorder(self)

    def run_with_recording(self):
        """Enhanced run method with recording capabilities."""
        clock = pygame.time.Clock()
        running = True
        while running:
            # The delta_time calculation normalizes frame rate to 60 updates per second
            # Each update advances the simulation by `time_multiplier` days.
            delta_time = clock.tick(60) / 1000.0 * 60

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

                    # Recording controls
                    if event.key == pygame.K_r:
                        current_speed = self.simulation_state.time_multiplier
                        print(f"Starting 5-second recording of the front view at {current_speed:.2f}x speed...")
                        self.recorder.start_recording('front', current_speed, 5, ['mp4'])

                    if event.key == pygame.K_b:
                        current_speed = self.simulation_state.time_multiplier
                        print(f"Starting 5-second recording of the back view at {current_speed:.2f}x speed...")
                        self.recorder.start_recording('back', current_speed, 5, ['mp4'])

                    if event.key == pygame.K_c:
                        current_speed = self.simulation_state.time_multiplier
                        # Calculate duration to record 365 simulation days
                        # Each second of recording at 60fps covers (60 * current_speed) days
                        duration = 365 / (60 * current_speed)
                        print(f"Starting 365-day cycle recording of the front view at {current_speed:.2f}x speed...")
                        self.recorder.start_recording('front', current_speed, duration, ['mp4'])

            if not self.recorder.recording:
                self.simulation_state.update(delta_time)

            self._draw_scene()
            pygame.display.flip()

        pygame.quit()
        sys.exit()

    ModernAntikythera.__original_init__ = ModernAntikythera.__init__
    ModernAntikythera.__init__ = __init_with_recorder__
    ModernAntikythera.run = run_with_recording


if __name__ == '__main__':
    try:
        import cv2
        from PIL import Image

        add_recording_to_main_app()
        print("Recording functionality enabled!")
        print("Press 'R' to record 5s of the front view at current speed.")
        print("Press 'B' to record 5s of the back view at current speed.")
        print("Press 'C' to record a full 365-day cycle of the front view.")
    except ImportError as e:
        print(f"Recording functionality disabled. Missing: {e}")
        print("Install with: pip install opencv-python pillow")

    app = ModernAntikythera()
    app.run()
