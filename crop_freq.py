import argparse
from pydub import AudioSegment


def remove_high_frequencies(audio_segment, cutoff_frequency):
    return audio_segment.low_pass_filter(cutoff_frequency, )


def remove_low_frequencies(audio_segment, cutoff_frequency):
    return audio_segment.high_pass_filter(cutoff_frequency)


def main():
    parser = argparse.ArgumentParser(description="Audio Frequency Filter")
    parser.add_argument("input_file", help="Input audio file path")
    parser.add_argument("output_file", help="Output audio file path")
    parser.add_argument("cutoff_frequency_high", type=int, help="Cutoff frequency for high-pass filter in Hz")
    parser.add_argument("cutoff_frequency_low", type=int, help="Cutoff frequency for low-pass filter in Hz")

    args = parser.parse_args()

    # Load the input audio file
    audio = AudioSegment.from_file(args.input_file)

    # Remove high frequencies
    modified_audio = remove_high_frequencies(audio, args.cutoff_frequency_high)
    # Remove low frequencies
    modified_audio = remove_low_frequencies(modified_audio, args.cutoff_frequency_low)

    # Export the modified audio to a new file
    modified_audio.export(args.output_file, format="mp3")


if __name__ == "__main__":
    main()
