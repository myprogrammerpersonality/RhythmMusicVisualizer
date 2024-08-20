#!/bin/bash

# Variables
FRAME_RATE=60
INPUT_FRAMES="frames/frame_%05d.png"
START_TIME=0
DURATION=60
SAMPLE_RATE=44100
BACK_RATE=0.01
RADIUS_FACTOR=10
WIDTH=1280   # Set the desired width
HEIGHT=720  # Set the desired height
AUDIO_FILE="../data/be_soo.mp3"
OUTPUT_VIDEO="outputs/output_video_60fps_audio.mp4"

# Rendering with PyGame Command
python game_render.py --file_path $AUDIO_FILE --duration $DURATION --fps $FRAME_RATE --sample_rate $SAMPLE_RATE --back_rate $BACK_RATE --radius_scaling_factor $RADIUS_FACTOR --width $WIDTH --height $HEIGHT

# Merging with FFmpeg Command
ffmpeg -r $FRAME_RATE -i $INPUT_FRAMES -s ${WIDTH}x${HEIGHT} -ss $START_TIME -t $DURATION -i $AUDIO_FILE -c:v libx264 -vf fps=$FRAME_RATE -pix_fmt yuv420p -c:a aac -shortest $OUTPUT_VIDEO