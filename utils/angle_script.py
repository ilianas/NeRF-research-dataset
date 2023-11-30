import json
import numpy as np
import os
import sys

def extract_euler_from_matrix(matrix):
    # Ensure it's a numpy array
    matrix = np.asarray(matrix)
    
    theta_y = np.arctan2(-matrix[2][0], np.sqrt(matrix[0][0]**2 + matrix[1][0]**2))
    theta_x = np.arctan2(matrix[2][1], matrix[2][2])
    theta_z = np.arctan2(matrix[1][0], matrix[0][0])

    # Convert angles from radians to degrees
    theta_x = np.degrees(theta_x)
    theta_y = np.degrees(theta_y)
    theta_z = np.degrees(theta_z)

    return theta_x, theta_y, theta_z

# Parsing command line arguments
if len(sys.argv) != 3:
    print("Please provide the paths to the transform JSON and result file.")
    print("Usage: python script.py path_to_transform_json path_to_result")
    sys.exit(1)

path_to_transform_json = sys.argv[1]
path_to_result = sys.argv[2]

with open(path_to_transform_json) as f:
    transform_json = json.load(f)
    
images_angles = dict()
for i in transform_json['frames']:
    images_angles[i['file_path']] = extract_euler_from_matrix(i['transform_matrix'])

result_file_path = os.path.join(path_to_result, f'{os.path.basename(os.path.dirname(path_to_transform_json))}_result.json')
with open(result_file_path, 'w', encoding='utf8') as f:
    json.dump(images_angles, f, indent=2, ensure_ascii=False)

print(f"Results saved to: {result_file_path}")