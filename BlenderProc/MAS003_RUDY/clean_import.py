import bpy, os, re
import numpy as np


ldr_file = 'MAS003_RUDY.ldr'
ldr_path = os.path.join(os.getcwd(), ldr_file)

import_ldraw_file = 'importldraw1.1.11_for_blender_281.zip'
import_ldraw_path = os.path.join(os.getcwd(), import_ldraw_file)

output_file = ldr_file.replace('.ldr', '.blend')
output_path = os.path.join(os.getcwd(), output_file)

# install LDraw Addon for importing Lego Models
bpy.ops.preferences.addon_install(filepath=import_ldraw_path, overwrite=True)
bpy.ops.preferences.addon_enable(module="io_scene_importldraw")
bpy.ops.wm.save_userpref()

# import model
bpy.ops.import_scene.importldraw(filepath=ldr_path, ldrawPath="/home/panda/LDraw/ldraw/")

# remove lego ground plane
bpy.context.collection.objects['LegoGroundPlane']
plane = bpy.context.active_object
bpy.ops.object.delete()
bpy.data.materials.remove( bpy.data.materials['Mat_LegoGroundPlane'])

# remove parent object and links
objects = bpy.data.objects
#objects.remove(objects['00000_' + ldr_file], do_unlink=True)
for obj in objects:
    if not obj.name.endswith('.dat'):
        print(f'Removing {obj.name}')
        objects.remove(obj, do_unlink=True)

# remove custom parts
custom_parts = ['00160_m898c3b67_202136_062848.dat', '00161_m898c3b67_202136_062819.dat']
for parts in custom_parts:
    print(f'Removing custom parts: {parts}')
    objects.remove(objects[parts])

# select random pieces from set
rng = np.random.default_rng()
keep_obj = rng.choice(objects, 60, replace=False)
for obj in objects:
    if obj not in keep_obj:
        print(f'Pruning objects, removing {obj.name}')
        objects.remove(obj, do_unlink=True)

# remove all lights
lights = bpy.data.lights
for light in lights:
    lights.remove(light)

# remove all cameras
cameras = bpy.data.cameras
for camera in cameras:
    cameras.remove(camera)

# create handle to all lego pieces
lego_pieces = [obj for obj in objects]

# add camera to scene
scene = bpy.context.scene
#scene.camera = cam
scene.render.image_settings.file_format='PNG'

# set render engine
scene.render.engine = 'CYCLES'
scene.cycles.device = 'GPU'
scene.cycles.use_denoising = True
#scene.cycles.denoiser = 'OPENIMAGEDENOISE'
scene.cycles.denoiser = 'OPTIX'
scene.cycles.use_preview_denoising = True


## render scene
#scene.render.filepath=f'output.png'
#bpy.ops.render.render(write_still=1)

# make single user
bpy.ops.object.make_single_user(type='ALL', object=True, obdata=True, material=False, animation=False)

# save blend file
bpy.ops.wm.save_as_mainfile(filepath=output_path)

# list classes
print('Class List')
classes = []
for obj in objects:
    n0 = re.sub('^[0-9]+_', '', obj.name)
    name  = re.sub('.dat', '', n0)
    if name not in classes:
        classes.append(name)

for cl in sorted(classes, key=lambda x: int(re.sub('[A-Za-z_]', '', x))):
    print(cl)

