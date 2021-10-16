#!/bin/bash

CONFIG_PATH=`pwd`
#BLENDER_PROC_PATH=/home/panda/LDraw/BlenderProc
BLEND_FILE=MAS003_RUDY.blend

#cd $BLENDER_PROC_PATH
NUM_IMAGES=5000
#NUM_IMAGES=2
for (( c=0; c<$NUM_IMAGES; c++ )); do
    #python run.py $CONFIG_PATH/config.yaml $CONFIG_PATH/camera_positions $CONFIG_PATH/$BLEND_FILE resources/cctextures $CONFIG_PATH/output
    blender --background --python clean_import.py
    blenderproc run main.py
done
