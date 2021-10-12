import bpy, os

# install LDraw Addon for importing Lego Models
p = os.path.abspath("importldraw1.1.11_for_blender_281.zip")
bpy.ops.preferences.addon_install(filepath=p, overwrite=True)
bpy.ops.preferences.addon_enable(module="io_scene_importldraw")
bpy.ops.wm.save_userpref()

# import model
bpy.ops.import_scene.importldraw(filepath="/home/panda/LDraw/Blender-Lego-Dataset/multiple.ldr", ldrawPath="/home/panda/LDraw/ldraw/")

# remove lego ground plane
bpy.context.collection.objects['LegoGroundPlane']
plane = bpy.context.active_object
bpy.ops.object.delete()
bpy.data.materials.remove( bpy.data.materials['Mat_LegoGroundPlane'])

# remove parent object and links
objects = bpy.data.objects
objects.remove(objects['00000_multiple.ldr'], do_unlink=True)

# remove all lights
lights = bpy.data.lights
for light in lights:
    lights.remove(light)

# create handle to all lego pieces
lego_pieces = [obj for obj in objects]

# add ground plane
bpy.ops.mesh.primitive_plane_add(size=50)
plane =  bpy.context.active_object

# create material on plan
#bpy.ops.material.new()
material = bpy.data.materials.new(name='PlaneMaterial')
material.use_nodes = True
plane.data.materials.append(material)
#bpy.data.objects.
#bpy.context.object.active_material.name = "PlaneMaterial"

##
# adding objects using bpy.ops library will automatically
# link it to the collection
##

## create light source
## other types of light sources: 
## https://docs.blender.org/manual/en/latest/render/lights/light_object.html#light-objects
#light_data = bpy.data.lights.new('light', type='POINT')
#light = bpy.data.objects.new('light', light_data)
#bpy.context.collection.objects.link(light)

## light location and energy
#light.location = (30, 20, 50)
#light.data.energy = 200.0

## we first create the camera object
#cam_data = bpy.data.cameras.new('camera')
#cam = bpy.data.objects.new('camera', cam_data)
#bpy.context.collection.objects.link(cam)
#cam.location=(0, 0, 20)

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

bpy.ops.wm.save_as_mainfile(filepath="/home/panda/LDraw/Blender-Lego-Dataset/generated_blend.blend")

