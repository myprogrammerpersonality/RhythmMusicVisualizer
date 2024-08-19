import pygame
import librosa
import sys
import time

# path
file_path = "../../data/be_soo.mp3"
duration = 60

# load music
y, sr = librosa.load(file_path, duration=duration)
y_harm, y_perc = librosa.effects.hpss(y)


# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Dynamic Circle")

# Define the array of radii (floats)
radii = [i * 10000 for i in y_perc]

# Define the time interval (in seconds) between radius updates
interval = 1 / sr

# Set the starting radius index
radius_index = 0

# Main loop
running = True
while running and radius_index < len(radii):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill((0, 0, 0))

    # Get the current radius from the array
    current_radius = radii[radius_index]

    # Draw the circle at the center of the screen
    pygame.draw.circle(screen, (255, 0, 0), (width // 2, height // 2), int(current_radius))

    # Update the display
    pygame.display.flip()

    # Wait for the next update
    time.sleep(interval)

    # Move to the next radius in the array
    radius_index += 1

# Quit Pygame
pygame.quit()
sys.exit()
