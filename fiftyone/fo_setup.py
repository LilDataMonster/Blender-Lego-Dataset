import fiftyone as fo
import os

# A name for the dataset
name = os.environ['NAME']

# The directory containing the dataset to import
dataset_dir = os.environ['DATASET_DIR']
labels_path = os.environ['LABELS_PATH']

# The type of the dataset being imported
dataset_type = fo.types.COCODetectionDataset  # for example
dataset = fo.load_dataset(name) if name in fo.list_datasets() else fo.Dataset.from_dir(dataset_dir=dataset_dir, dataset_type=dataset_type, labels_path=labels_path, name=name)

session = fo.launch_app(dataset, remote=True)
port = os.environ['FIFTYONE_DEFAULT_APP_PORT']
print(f'Session started on port {port}')
session.wait()
