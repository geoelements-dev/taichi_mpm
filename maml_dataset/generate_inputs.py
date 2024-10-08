import json
import os
import random

# Set the random seed for reproducibility
random.seed(404)

# Load the original inputs_2d file
with open('./maml_dataset/inputs_2d.json', 'r') as file:
    data = json.load(file)


def random_cube_space():
    """
    Generate a random cube space within specified bounds.

    Returns:
        list: A list containing one cube's [x, y, width, height] where
        x and y are randomly generated between 0.1 and 0.6, and width 
        and height are fixed at 0.3.
    """
    return [[random.uniform(0.1, 0.6), random.uniform(0.1, 0.6), 0.3, 0.3]]


def random_velocity():
    """
    Generate a random velocity vector.

    Returns:
        list: A list containing a random velocity vector [vx, vy],
        where vx and vy are random values between -1 and 1.
    """
    return [[random.uniform(-1, 1), random.uniform(-1, 1)]]


def create_files(base_data, start_angle, end_angle, increment, output_dir, n_files_per_angle):
    """
    Create multiple JSON files with varying friction angles and randomized cube properties.

    Args:
        base_data (dict): The base dictionary structure to modify and save for each file.
        start_angle (int): The starting value of the friction angle.
        end_angle (int): The ending value of the friction angle.
        increment (int): The step size to increment the friction angle between files.
        output_dir (str): The directory where the generated files will be saved.
        n_files_per_angle (int): The number of files to generate for each friction angle.

    Raises:
        OSError: If the output directory cannot be created.

    Side Effects:
        Creates a directory if it doesn't exist and writes JSON files to disk.
    """
    
    # Check if the output directory exists, if not, create it
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Loop over the range of angles (from start_angle to end_angle)
    for angle in range(start_angle, end_angle + 1, increment):
        
        # For each angle, generate `n_files_per_angle` files
        for i in range(n_files_per_angle):
            # Copy the base data to a new variable
            new_data = base_data.copy()

            # Update the friction angle
            new_data["friction_angle"] = angle

            # Set a fixed cube space and zero velocity for the first file
            new_data["gen_cube_from_data"]["sim_inputs"][0]["mass"]["cubes"] = random_cube_space()
            new_data["gen_cube_from_data"]["sim_inputs"][0]["mass"]["velocity_for_cubes"] = [[0, 0]]

            # Create the filename and file path for the first file
            filename = f"{angle}_0_{i}.json"
            filepath = os.path.join(output_dir, filename)

            # Update the save path in the JSON data
            new_data["save_path"] = os.path.join(output_dir, f"{angle}_0_{i}/")

            # Write the first JSON file with the modified data
            with open(filepath, 'w') as outfile:
                json.dump(new_data, outfile, indent=4)
            
            print(f"Created file: {filename}")

            # Set new random cube space and velocity for the second file
            new_data["gen_cube_from_data"]["sim_inputs"][0]["mass"]["cubes"] = random_cube_space()
            new_data["gen_cube_from_data"]["sim_inputs"][0]["mass"]["velocity_for_cubes"] = random_velocity()

            # Create the filename and file path for the second file
            filename = f"{angle}_1_{i}.json"
            filepath = os.path.join(output_dir, filename)

            # Update the save path in the JSON data for the second file
            new_data["save_path"] = os.path.join(output_dir, f"{angle}_1_{i}/")

            # Write the second JSON file with the modified data
            with open(filepath, 'w') as outfile:
                json.dump(new_data, outfile, indent=4)
            
            print(f"Created file: {filename}")


# Set parameters for file generation
start_angle = 20       # Starting friction angle
end_angle = 40         # Ending friction angle
increment = 5          # Increment of friction angle between files
n_files_per_angle = 5   # Number of files to generate per friction angle
output_directory = './maml_dataset/dataset/'  # Directory to save generated files

# Call the function to create the JSON files
create_files(data, start_angle, end_angle, increment, output_directory, n_files_per_angle)
