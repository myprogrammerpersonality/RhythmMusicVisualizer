import argparse
import logging
import time
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np


def plot_spectrogram(file_path, sample_rate, freq_lines):
    # Load the audio file using librosa
    start_time = time.time()
    y, sr = librosa.load(file_path, sr=sample_rate)
    logging.info(f"Loading audio took {time.time() - start_time} seconds")

    # Generate the spectrogram
    start_time = time.time()
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
    logging.info(f"Generating spectrogram took {time.time() - start_time} seconds")

    # Display the spectrogram
    plt.figure(figsize=(10, 5))
    start_time = time.time()
    librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='log')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Spectrogram of ' + file_path)

    # Plot freq lines at specified frequencies
    for freq in freq_lines:
        plt.axhline(y=freq, color='cyan', linestyle='--', linewidth=0.5)

    plt.show()
    logging.info(f"Displaying spectrogram took {time.time() - start_time} seconds")


def main():
    parser = argparse.ArgumentParser(description="Audio Spectrogram Plotter")
    parser.add_argument("file_path", help="Path to the audio file")
    parser.add_argument("--sample_rate", type=int, default=None, help="Sample rate for audio file")
    parser.add_argument("--freq_lines", nargs='+', type=int,
                        default=[132, 174, 196, 213, 233, 261, 286, 310, 319, 349, 349, 391, 427,
                                 466, 524, 587, 622, 638, 697, 698, 782, 854, 932, 1048, 1174, 1244, 1394],
                        help="List of frequencies to mark on the spectrogram")

    args = parser.parse_args()

    plot_spectrogram(args.file_path, args.sample_rate, args.freq_lines)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
