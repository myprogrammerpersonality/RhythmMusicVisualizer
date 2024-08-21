#!/bin/bash

# Variables
FRAME_RATE=60
INPUT_FRAMES="frames/frame_%05d.png"
START_TIME=0
DURATION=120
SAMPLE_RATE=44100
BACK_RATE=0.1
RADIUS_FACTOR=10
WIDTH=720   # Set the desired width
HEIGHT=480  # Set the desired height
AUDIO_FILE="../data/Taylor-Swift-Style-320.mp3"
OUTPUT_VIDEO="outputs/Taylor-Swift-Style-320_60fps_480p_mp_batch.mp4"

# Rendering with PyGame Command
python game_render_mp_batch.py --file_path $AUDIO_FILE --duration $DURATION --fps $FRAME_RATE --sample_rate $SAMPLE_RATE --back_rate $BACK_RATE --radius_scaling_factor $RADIUS_FACTOR --width $WIDTH --height $HEIGHT

# Merging with FFmpeg Command
ffmpeg -r $FRAME_RATE -i $INPUT_FRAMES -ss $START_TIME -t $DURATION -i $AUDIO_FILE -c:v libx264 -vf fps=$FRAME_RATE -pix_fmt yuv420p -c:a aac -shortest $OUTPUT_VIDEO
