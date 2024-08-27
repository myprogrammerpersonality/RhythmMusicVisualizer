#!/bin/bash

# Variables
FRAME_RATE=60
INPUT_FRAMES="frames/frame_%05d.png"
START_TIME=0
DURATION=120
SAMPLE_RATE=44100
BACK_RATE=0.1
RADIUS_FACTOR=10
WIDTH=1024   # Set the desired width
HEIGHT=720  # Set the desired height
AUDIO_FILE="../data/7-Chaharmezrab_Shahnaz.mp3"
OUTPUT_VIDEO="outputs/7-Chaharmezrab_Shahnaz_60fps_720p_mp.mp4"

# Rendering with PyGame Command
python game_render_mp.py --file_path $AUDIO_FILE --duration $DURATION --fps $FRAME_RATE --sample_rate $SAMPLE_RATE --back_rate $BACK_RATE --radius_scaling_factor $RADIUS_FACTOR --width $WIDTH --height $HEIGHT

# Merging with FFmpeg Command
ffmpeg -r $FRAME_RATE -i $INPUT_FRAMES -ss $START_TIME -t $DURATION -i $AUDIO_FILE -c:v libx264 -vf fps=$FRAME_RATE -pix_fmt yuv420p -c:a aac -shortest $OUTPUT_VIDEO
