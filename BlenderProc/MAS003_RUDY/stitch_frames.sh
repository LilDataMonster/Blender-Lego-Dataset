ffmpeg -framerate 1 -i output/coco_data/images/%06d.jpg -c:v libx264 -profile:v high -crf 20 -pix_fmt yuv420p output.mp4
