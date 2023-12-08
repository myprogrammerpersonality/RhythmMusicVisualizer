import argparse
import logging
import time
import librosa.display
import matplotlib.pyplot as plt
import numpy as np


def plot_spectrogram(file_path, sample_rate):
    # Load the audio file using librosa
    start_time = time.time()
    y, sr = librosa.load(file_path, sr=sample_rate)
    logging.info(f"Loading audio took {time.time() - start_time} seconds")

    # Generate the spectrogram
    start_time = time.time()
    D = librosa.amplitude_to_db(librosa.stft(y), ref=np.max)
    logging.info(f"Generating spectrogram took {time.time() - start_time} seconds")

    # Display the spectrogram
    plt.figure(figsize=(10, 5))
    start_time = time.time()
    librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='log')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Spectrogram of ' + file_path)
    plt.show()
    logging.info(f"Displaying spectrogram took {time.time() - start_time} seconds")


def main():
    parser = argparse.ArgumentParser(description="Audio Spectrogram Plotter")
    parser.add_argument("file_path", help="Path to the audio file")
    parser.add_argument("--sample_rate", type=int, default=None, help="Sample rate for audio file")

    args = parser.parse_args()

    plot_spectrogram(args.file_path, args.sample_rate)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
