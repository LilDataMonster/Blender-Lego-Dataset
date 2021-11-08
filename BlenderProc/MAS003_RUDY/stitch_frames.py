import ffmpeg

(
    ffmpeg
    .input('output/coco_data_vid0/images/*.jpg', pattern_type='glob', framerate=10)
    #.filter('deflicker', mode='pm', size=10)
    #.filter('scale', size='hd1080', force_original_aspect_ratio='increase')
    #.output('movie.mp4', crf=20, preset='slower', movflags='faststart', pix_fmt='yuv420p')
    #.filter("minterpolate='mi_mode=mci:mc_mode=aobmc:vsbmc=1'")
    .filter("minterpolate", mi_mode="mci", mc_mode="aobmc", vsbmc=1)
    .output('movie.mp4', crf=20, preset='slower', pix_fmt='yuv420p', vcodec='h264')
    #.overwrite_output()
    #.view(filename='filter_graph')
    .run()
)
