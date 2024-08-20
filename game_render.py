import sys
import os
import logging
import argparse
import pygame
import librosa


# Configure logger to show date and time
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


# Set up command-line arguments
parser = argparse.ArgumentParser(description="Render audio visualization frames using Pygame.")
parser.add_argument('--file_path', type=str, required=True, help='Path to the audio file')
parser.add_argument('--duration', type=int, default=60, help='Duration of audio to load in seconds')
parser.add_argument('--fps', type=int, default=60, help='Frames per second')
parser.add_argument('--sample_rate', type=int, default=44100, help='Sample rate of the audio')
parser.add_argument('--back_rate', type=float, default=0.01, help='Rate at which the adjustment value decreases')
parser.add_argument('--radius_scaling_factor', type=float, default=10, help='Scaling factor for the circle radius')
parser.add_argument('--width', type=int, default=800, help='Frames Width')
parser.add_argument('--height', type=int, default=600, help='Frames Height')

args = parser.parse_args()
window_size = args.sample_rate // args.fps


# Create an output directory for frames
output_dir = "frames"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    logging.info("Created the frames folder!")


# Load music
y, sr = librosa.load(args.file_path, duration=args.duration, sr=args.sample_rate)
y_harm, y_perc = librosa.effects.hpss(y)

logging.info("Loaded the music.")

adj_val = 0
new_vals = []

for val in y_perc:
    if val > 0:
        adj_val += val
    adj_val -= args.back_rate
    if adj_val < 0:
        adj_val = 0
    new_vals.append(adj_val)

new_vals_compressed = []
i = 0
while i < len(new_vals):
    val = max(new_vals[i:i+window_size])
    new_vals_compressed.append(val * args.radius_scaling_factor)
    i += window_size

logging.info(f"Proccessing Finished. len new vals: {len(new_vals_compressed)}")

# Initialize Pygame
pygame.init()

# Set up the display (you won't actually see this, it's for frame rendering)
width, height = args.width, args.height
screen = pygame.display.set_mode((width, height))

# Define the array of radii (floats)
radii = new_vals_compressed

# Set the starting radius index
radius_index = 0

# Main loop for rendering frames
frame_number = 0
while radius_index < len(radii):
    if radius_index%100==0:
        logging.info(f"Frame {radius_index} / {len(radii)}")
    # Clear the screen
    screen.fill((0, 0, 0))

    # Get the current radius from the array
    current_radius = radii[radius_index]

    # Draw the circle at the center of the screen
    pygame.draw.circle(screen, (255, 0, 0), (width // 2, height // 2), int(current_radius))

    # Save the frame as an image
    frame_filename = os.path.join(output_dir, f"frame_{frame_number:05d}.png")
    pygame.image.save(screen, frame_filename)

    # Move to the next radius in the array
    radius_index += 1
    frame_number += 1

logging.info("Rendering Finished!")

# Quit Pygame
pygame.quit()
sys.exit()
