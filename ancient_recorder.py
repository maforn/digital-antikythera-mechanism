import pygame
import numpy as np
import cv2
import os
from PIL import Image
from datetime import datetime
from ancient_simulation import AncientAntikythera
import sys
import math


class AncientSimulationRecorder:
    """Records the ancient simulation to GIF and MP4 formats."""

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
        original_speed = self.app.state.time_multiplier
        original_paused = self.app.state.paused

        self.app.current_view = view
        self.app.state.time_multiplier = speed_multiplier
        self.app.state.paused = False
        self.app._update_caption()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        speed_name = f"speed_{speed_multiplier:.2f}x".replace('.', '_')
        base_filename = f"ancient_{view}_{speed_name}_{timestamp}"

        if 'mp4' in formats:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            mp4_path = os.path.join(self.output_dir, f"{base_filename}.mp4")
            self.video_writer = cv2.VideoWriter(mp4_path, fourcc, 60.0,
                                                (self.app.WIDTH, self.app.HEIGHT))

        print(f"Recording {view} view at {speed_multiplier:.2f}x speed for {duration_seconds:.2f} seconds...")

        frames_to_record = int(duration_seconds * 60)  # 60 FPS

        for frame_num in range(frames_to_record):
            self.app.state.update()  # Use the ancient simulation's update method

            self.app._draw_scene()
            pygame.display.flip()

            frame_surface = pygame.display.get_surface()
            frame_array = pygame.surfarray.array3d(frame_surface)
            frame_array = np.rot90(frame_array)
            frame_array = np.flipud(frame_array)

            if 'mp4' in formats and self.video_writer:
                frame_bgr = cv2.cvtColor(frame_array, cv2.COLOR_RGB2BGR)
                self.video_writer.write(frame_bgr)

            if (frame_num + 1) % 60 == 0:
                print(f"Recorded {(frame_num + 1) // 60} seconds...")

        if self.video_writer:
            self.video_writer.release()
            print(f"MP4 saved: {mp4_path}")

        self.app.current_view = original_view
        self.app.state.time_multiplier = original_speed
        self.app.state.paused = original_paused
        self.app._update_caption()

        self.recording = False
        self.frames = []
        print("Recording completed!")


def add_recording_to_ancient_app():
    """Add recording functionality to the main AncientAntikythera class."""

    def __init_with_recorder__(self):
        self.__original_init__()
        self.recorder = AncientSimulationRecorder(self)

    def run_with_recording(self):
        """Enhanced run method with recording capabilities."""
        while True:
            if not self.recorder.recording:
                self._handle_input_with_recording()
                self.state.update()

            self._draw_scene()
            self.clock.tick(60)

    def _handle_input_with_recording(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.state.change_speed(1.5)
                elif event.key == pygame.K_DOWN:
                    self.state.change_speed(1 / 1.5)
                elif event.key == pygame.K_SPACE:
                    self.state.toggle_pause()
                elif event.key == pygame.K_TAB:
                    self.current_view = 'back' if self.current_view == 'front' else 'front'
                    self._update_caption()

                # Recording controls
                elif event.key == pygame.K_r:
                    current_speed = self.state.time_multiplier
                    print(f"Starting 5-second recording of the front view at {current_speed:.2f}x speed...")
                    self.recorder.start_recording('front', current_speed, 5, ['mp4'])

                elif event.key == pygame.K_b:
                    current_speed = self.state.time_multiplier
                    print(f"Starting 5-second recording of the back view at {current_speed:.2f}x speed...")
                    self.recorder.start_recording('back', current_speed, 5, ['mp4'])

                elif event.key == pygame.K_c:
                    current_speed = self.state.time_multiplier
                    # Each frame advances by 'current_speed' days. At 60fps, one second is 60*current_speed days.
                    duration = 365.25 / (60 * current_speed)
                    print(f"Starting 365-day cycle recording of the front view at {current_speed:.2f}x speed...")
                    self.recorder.start_recording('front', current_speed, duration, ['mp4'])

    # Monkey patch the AncientAntikythera class
    AncientAntikythera.__original_init__ = AncientAntikythera.__init__
    AncientAntikythera.__init__ = __init_with_recorder__
    AncientAntikythera.run = run_with_recording
    AncientAntikythera._handle_input_with_recording = _handle_input_with_recording

    # Replace original _handle_input with a placeholder to avoid conflicts
    AncientAntikythera._handle_input = lambda self: self._handle_input_with_recording()


if __name__ == '__main__':
    try:
        import cv2
        from PIL import Image

        add_recording_to_ancient_app()
        print("Recording functionality enabled for Ancient Simulation!")
        print("Press 'R' to record 5s of the front view at current speed.")
        print("Press 'B' to record 5s of the back view at current speed.")
        print("Press 'C' to record a full 365-day cycle of the front view.")
    except ImportError as e:
        print(f"Recording functionality disabled. Missing: {e}")
        print("Install with: pip install opencv-python pillow")

    app = AncientAntikythera()
    app.run()
