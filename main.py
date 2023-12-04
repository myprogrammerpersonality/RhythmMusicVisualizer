import argparse
import librosa.display
import matplotlib.pyplot as plt
import numpy as np


def plot_spectrogram(file_path):
    # Load the audio file using librosa
    y, sr = librosa.load(file_path, sr=None)

    print("sr: ", sr)

    # Generate the spectrogram
    D = librosa.amplitude_to_db(librosa.stft(y), ref=np.max)

    # Display the spectrogram
    plt.figure(figsize=(10, 5))
    librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='log')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Spectrogram of ' + file_path)
    plt.show()


def main():
    parser = argparse.ArgumentParser(description="Audio Spectrogram Plotter")
    parser.add_argument("file_path", help="Path to the audio file")

    args = parser.parse_args()

    plot_spectrogram(args.file_path)


if __name__ == "__main__":
    main()
