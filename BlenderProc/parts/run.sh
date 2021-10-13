#!/bin/bash

cd /home/panda/LDraw/BlenderProc

for (( c=1; c<=10; c++ )); do
    python run.py ../Blender-Lego-Dataset/BlenderProc/parts/config.yaml ../Blender-Lego-Dataset/BlenderProc/parts/camera_positions ../Blender-Lego-Dataset/BlenderProc/parts/generated_blend.blend resources/cctextures ../Blender-Lego-Dataset/BlenderProc/parts/output
done
