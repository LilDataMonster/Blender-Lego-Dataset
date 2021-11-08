import numpy as np
import pandas as pd

points = []

# list keypoints using [x, y, z, rotx, roty, rotz], num_interpolation_points
# where the the number of interpolation points are the number of points between
# the current and previous keypoints
keypoints = [
    ([0, -1, 3, 0.1, 0, 0], 0),
    ([0, -4, 3, 0.1, 0, 0], 30),
    ([-4, -4, 3, 0.1, 0, 0], 30),
    ([-4, -2, 3, 0.1, 0, 0], 30),
    ([-4, 3, 3, 0.1, 0, 0], 30),
    ([-4, 3, 3, 0.1, 0, 0], 30),
    ([3, 3, 3, 0.1, 0, 0], 30),
    ([5, 3, 3, 0.1, 0, 0], 30),
]

last_keypoint, _ = keypoints[0]
for key, interp_points in keypoints:
    # handle first point (maybe just do enumerated index?)
    if np.all(key == last_keypoint):
        points.append(np.array(key))
        last_keypoint = key
        continue

    # use linspace to evenly distribute between two arrays, a given number of points
    # ignore the fist point as it will be a copy from the previous run
    new_points = np.linspace(last_keypoint, key, interp_points)[1:]
    last_keypoint = key

    #print(new_points)
    points.extend(new_points)

#print(points)
#print(np.shape(points))

df = pd.DataFrame(points)
df.to_csv('camera_positions1', sep=' ', index=False, header=False, float_format='%.3f')
print(df)
