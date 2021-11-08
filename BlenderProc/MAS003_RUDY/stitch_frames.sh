#ffmpeg -framerate 10 -i output/coco_data/images/%06d.jpg -c:v libx264 -filter:v "minterpolate='mi_mode=mci:mc_mode=aobmc:vsbmc=1:fps=120'" -profile:v high -crf 20 -pix_fmt yuv420p output.mp4
ffmpeg -framerate 10 -i output/coco_data/images/%06d.jpg -c:v libx264 -filter:v "minterpolate='mi_mode=mci:mc_mode=aobmc:vsbmc=1'" -r 30 -profile:v high -crf 20 -pix_fmt yuv420p output.mp4
