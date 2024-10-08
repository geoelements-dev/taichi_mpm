import json
import os
import random

random.seed(404)

# Load the original inputs_2d file
with open('./maml_dataset/inputs_2d.json', 'r') as file:
    data = json.load(file)

def random_cube_space():
    return [[random.uniform(0.1, 0.6), random.uniform(0.1, 0.6), 0.3, 0.3]]

def random_velocity():
    return[[random.uniform(-1,1), random.uniform(-1,1)]]


# Function to create new files with varying friction_angle
def create_files(base_data, start_angle, end_angle, increment, output_dir, n_files_per_angle):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for angle in range(start_angle, end_angle + 1, increment):
        for i in range(n_files_per_angle):
            # Update the friction_angle
            new_data = base_data.copy()
            new_data["friction_angle"] = angle
            
            # Generate random cube_gen_space
            new_data["gen_cube_from_data"]["sim_inputs"][0]["mass"]["cubes"] = random_cube_space()
            new_data["gen_cube_from_data"]["sim_inputs"][0]["mass"]["velocity_for_cubes"] = [[0,0]]

            # Save the modified data to a new file
            filename = f"{angle}_0_{i}.json"
            filepath = os.path.join(output_dir, filename)

            new_data["save_path"] = os.path.join(output_dir, f"{angle}_0_{i}/")
            
            with open(filepath, 'w') as outfile:
                json.dump(new_data, outfile, indent=4)
            
            print(f"Created file: {filename}")

            new_data["gen_cube_from_data"]["sim_inputs"][0]["mass"]["cubes"] = random_cube_space()
            new_data["gen_cube_from_data"]["sim_inputs"][0]["mass"]["velocity_for_cubes"] = random_velocity()

            filename = f"{angle}_1_{i}.json"
            filepath = os.path.join(output_dir, filename)

            new_data["save_path"] = os.path.join(output_dir, f"{angle}_1_{i}/")

            with open(filepath, 'w') as outfile:
                json.dump(new_data, outfile, indent=4)
            
            print(f"Created file: {filename}")


# Set parameters
start_angle = 20
end_angle = 40
increment = 5
n_files_per_angle = 5
output_directory = './maml_dataset/dataset/'

# Create the files
create_files(data, start_angle, end_angle, increment, output_directory, n_files_per_angle)