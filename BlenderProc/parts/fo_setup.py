import fiftyone as fo

# A name for the dataset
name = "lego"

# The directory containing the dataset to import
dataset_dir = "/home/panda/LDraw/Blender-Lego-Dataset/BlenderProc/lego/output/"
#dataset_dir = "/home/panda/LDraw/Blender-Lego-Dataset/BlenderProc/lego/output/coco_data/"
#labels_path = "/home/panda/LDraw/Blender-Lego-Dataset/BlenderProc/lego/output/coco_annotations.json"
labels_path = "/home/panda/LDraw/Blender-Lego-Dataset/BlenderProc/lego/output/coco_data/coco_annotations.json"

# The type of the dataset being imported
dataset_type = fo.types.COCODetectionDataset  # for example

dataset = fo.Dataset.from_dir(
    dataset_dir=dataset_dir,
    dataset_type=dataset_type,
    labels_path=labels_path,
    name=name,
)

session = fo.launch_app(dataset)
session.wait()
