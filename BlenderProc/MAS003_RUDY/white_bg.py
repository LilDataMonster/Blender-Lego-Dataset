import blenderproc as bproc
import argparse
import numpy as np
import os, re


parser = argparse.ArgumentParser()
parser.add_argument('camera', nargs='?', default="camera_positions", help="Path to the camera file")
parser.add_argument('scene', nargs='?', default="MAS003_RUDY.blend", help="Path to the scene.blend file")
parser.add_argument('cc_material_path', nargs='?', default="resources/cctextures", help="Path to CCTextures folder, see the /scripts for the download script.")
parser.add_argument('output_dir', nargs='?', default="output", help="Path to where the final files will be saved ")
args = parser.parse_args()

append_to_existing_output = True

bproc.init()

####################################
# load the objects into the scene
####################################
objs = bproc.loader.load_blend(args.scene)

# Make all spheres actively participate in the simulation
for obj in objs:
    category_id = re.sub('^[0-9]+_', '', obj.get_name())
    category_id = re.sub('.dat', '', category_id)
    category_id = re.sub('b', '', category_id) # remove 'b'
    print(f'Setting {obj.get_name()} to category {category_id}')
    obj.set_cp("category_id", category_id)
    obj.enable_rigidbody(active=True)
    # print(dir(obj))

####################################
# Define a light
####################################
print('Setting up lighting')
light = bproc.types.Light()
light.set_type("POINT")
# Sample its location in a shell around the point [0, 0, 0]
light.set_location(bproc.sampler.shell(
    center=[
        np.random.uniform(-1,1),
        np.random.uniform(-1,1),
        np.random.uniform(-1,1),
        ],
    radius_min=30,
    radius_max=50,
    elevation_min=20,
    elevation_max=30
))
light.set_energy(15000)

#####################################
## Define a light
#####################################
#print('Setting up lighting')
#lightr = bproc.types.Light()
#lightr.set_type("POINT")
## Sample its location in a shell around the point [0, 0, 0]
#lightr.set_location(bproc.sampler.shell(
#    center=[1.5, 0, 0],
#    radius_min=30,
#    radius_max=50,
#    elevation_min=55,
#    elevation_max=89
#))
#lightr.set_energy(15000)

####################################
# define the camera intrinsics
####################################
print('Setting up camera')
bproc.camera.set_resolution(1280, 720)
bproc.camera.set_intrinsics_from_blender_params(lens=2, lens_unit='FOV')

# read the camera positions file and convert into homogeneous camera-world transformation
with open(args.camera, "r") as f:
    for line in f.readlines():
        line = [float(x) for x in line.split()]
        position, euler_rotation = line[:3], line[3:6]
        matrix_world = bproc.math.build_transformation_mat(position, euler_rotation)
        bproc.camera.add_camera_pose(matrix_world)

####################################
# load all recommended cc materials
####################################
print('Setting up materials')
cc_used_assets = ["Tile", "Fabric", "Concrete",
                  "Paint", "Plastic",
                  "Plaster", "Paper", "Porcelain" ]
cc_textures = bproc.loader.load_ccmaterials(args.cc_material_path,
                                            used_assets=cc_used_assets)

####################################
# create the ground
####################################
print('Setting up ground plane')
ground_plane = bproc.object.create_primitive('PLANE', scale=[10, 6, 1])

# The ground should only act as an obstacle and is therefore marked passive.
# To let the spheres fall into the valleys of the ground, make the collision shape MESH instead of CONVEX_HULL.
ground_plane.enable_rigidbody(active=False, collision_shape="MESH")

# define a function that samples the initial pose of a given object above the ground
def sample_initial_pose(obj: bproc.types.MeshObject):
    obj.set_location(bproc.sampler.upper_region(objects_to_sample_on=ground_plane,
                                                min_height=1, max_height=2))#, face_sample_range=[0.4, 0.6]))
    # obj.set_location(np.random.uniform([-2.5, -1.5, -0.2], [2.5, 1.5, 0.2]))
    obj.set_rotation_euler(np.random.uniform([0, 0, 0], [np.pi, np.pi, np.pi]))

for _ in range(1):
    ## reset
    #bproc.utility.reset_keyframes()

    # texture ground plane
    random_cc_texture = np.random.choice(cc_textures)
    ground_plane.replace_materials(random_cc_texture)


    ####################################
    # sample objects ontop of surface
    ####################################
    print('Setting up object positioning')
    # sample objects on the given surface
    placed_objects = bproc.object.sample_poses_on_surface(objects_to_sample=objs,
                                                          surface=ground_plane,
                                                          sample_pose_func=sample_initial_pose,
                                                          min_distance=0.8,
                                                          max_distance=5)

    ####################################
    # physics positioning
    ####################################
    print('Setting up simulated physics')
    bproc.object.simulate_physics_and_fix_final_poses(min_simulation_time=2,
                                                      max_simulation_time=20,
                                                      check_object_interval=1,
                                                      substeps_per_frame = 20,
                                                      solver_iters=25)

    ####################################
    # Render
    ####################################
    print('Setting up render')
    # activate distance rendering and set amount of samples for color rendering
    # bproc.renderer.enable_distance_output()
    # bproc.renderer.enable_normals_output()
    bproc.renderer.set_samples(400)

    # render the whole pipeline
    data = bproc.renderer.render()

    # Render segmentation masks (per class and per instance)
    seg_data = bproc.renderer.render_segmap(map_by=["class", "instance"])
    data.update(seg_data)
    # # Convert distance to depth
    # data["depth"] = bproc.postprocessing.dist2depth(data["distance"])
    # del data["distance"]

    ####################################
    # write data
    ####################################
    print('Setting up file saves')

    # # write the data to a .hdf5 container
    # bproc.writer.write_hdf5(args.output_dir,
    #                         data,
    #                         append_to_existing_output=append_to_existing_output)

    # Write data to coco file
    bproc.writer.write_coco_annotations(os.path.join(args.output_dir, 'coco_data'),
                            instance_segmaps=seg_data["instance_segmaps"],
                            instance_attribute_maps=seg_data["instance_attribute_maps"],
                            colors=data["colors"],
                            color_file_format="JPEG",
                            append_to_existing_output=append_to_existing_output,
                            jpg_quality=100)
