import sys
import os
import logging
import argparse
import pygame
import librosa
import multiprocessing as mp


def render_frames(start, end, radii, width, height, output_dir, batch_size=10):
    pygame.init()
    screen = pygame.Surface((width, height))
    frames = []

    for i in range(start, end):
        screen.fill((0, 0, 0))
        current_radius = radii[i]
        pygame.draw.circle(screen, (255, 0, 0), (width // 2, height // 2), int(current_radius))
        
        # Store the frame in memory
        frame_surface = screen.copy()
        frames.append((frame_surface, i))

        # Save frames in batches
        if len(frames) >= batch_size:
            for frame_surface, frame_index in frames:
                frame_filename = os.path.join(output_dir, f"frame_{frame_index:05d}.png")
                pygame.image.save(frame_surface, frame_filename)
            frames.clear()  # Clear the list after saving

    # Save any remaining frames that didn't fill a complete batch
    for frame_surface, frame_index in frames:
        frame_filename = os.path.join(output_dir, f"frame_{frame_index:05d}.png")
        pygame.image.save(frame_surface, frame_filename)

    pygame.quit()


def main(args):
    # Configure logger
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

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

    logging.info(f"Processing Finished. len new vals: {len(new_vals_compressed)}")

    # Set the number of processes
    num_processes = mp.cpu_count()

    # Calculate chunk size
    chunk_size = len(new_vals_compressed) // num_processes
    processes = []

    # Batch size for saving frames
    batch_size = 100

    for i in range(num_processes):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i != num_processes - 1 else len(new_vals_compressed)
        p = mp.Process(target=render_frames, args=(start, end, new_vals_compressed, args.width, args.height, output_dir, batch_size))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    logging.info("Rendering Finished!")

if __name__ == "__main__":
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
    main(args)
