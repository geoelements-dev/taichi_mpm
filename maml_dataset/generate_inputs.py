import json
import os
import random
import hydra
from omegaconf import DictConfig, OmegaConf
from maml_dataset.args import Config
from typing import List, Dict

def random_cube_space() -> List[List[float]]:
    """
    Generate a random cube space within specified bounds.

    Returns:
        List[List[float]]: A list containing one cube's [x, y, width, height] where
        x and y are randomly generated between 0.1 and 0.6, and width and height are fixed at 0.3.
    """
    return [[random.uniform(0.1, 0.6), random.uniform(0.1, 0.6), 0.3, 0.3]]


def random_velocity() -> List[List[float]]:
    """
    Generate a random velocity vector.

    Returns:
        List[List[float]]: A list containing a random velocity vector [vx, vy],
        where vx and vy are random values between -1 and 1.
    """
    return [[random.uniform(-1, 1), random.uniform(-1, 1)]]


def create_files(base_data: Dict, cfg: DictConfig) -> None:
    """
    Create multiple JSON files with varying friction angles and randomized cube properties.

    Args:
        base_data (Dict): The base dictionary structure to modify and save for each file.
        cfg (DictConfig): The configuration object containing parameters for friction angle range, 
                          number of files to generate, and output directory settings.

    Side Effects:
        Creates a directory if it doesn't exist and writes JSON files to disk.
    """
    # Loop over the range of angles (from start_angle to end_angle)
    for angle in range(cfg.friction_angle.start_angle, cfg.friction_angle.end_angle + 1, cfg.friction_angle.increment):

        # For each angle, generate `n_files_per_angle` files
        for i in range(cfg.friction_angle.n_files):
            # Copy the base data to a new variable to avoid modifying the original
            new_data = base_data.copy()

            # Update the friction angle in the new data
            new_data["friction_angle"] = angle

            # Set a fixed cube space and zero velocity for the first file
            new_data["gen_cube_from_data"]["sim_inputs"][0]["mass"]["cubes"] = random_cube_space()
            new_data["gen_cube_from_data"]["sim_inputs"][0]["mass"]["velocity_for_cubes"] = [[0, 0]]

            # Create the filename and file path for the first file
            filename = f"{angle}_0_{i}.json"
            filepath = os.path.join(cfg.output_path, filename)

            # Update the save path in the JSON data
            new_data["save_path"] = os.path.join(cfg.output_path, f"{angle}_0_{i}/")

            # Write the first JSON file with the modified data
            with open(filepath, 'w') as outfile:
                json.dump(new_data, outfile, indent=4)

            print(f"Created file: {filename}")

            # Set new random cube space and velocity for the second file
            new_data["gen_cube_from_data"]["sim_inputs"][0]["mass"]["cubes"] = random_cube_space()
            new_data["gen_cube_from_data"]["sim_inputs"][0]["mass"]["velocity_for_cubes"] = random_velocity()

            # Create the filename and file path for the second file
            filename = f"{angle}_1_{i}.json"
            filepath = os.path.join(cfg.output_path, filename)

            # Update the save path in the JSON data for the second file
            new_data["save_path"] = os.path.join(cfg.output_path, f"{angle}_1_{i}/")

            # Write the second JSON file with the modified data
            with open(filepath, 'w') as outfile:
                json.dump(new_data, outfile, indent=4)

            print(f"Created file: {filename}")


@hydra.main(version_base=None, config_path=".", config_name="config")
def main(cfg: Config) -> None:
    """
    Main function to load base data and generate JSON files based on configuration settings.

    Args:
        cfg (Config): Configuration object from Hydra, containing input and output paths,
                      friction angle parameters, and random velocity settings.

    Side Effects:
        Loads data from input_path, creates output directories, and generates multiple JSON files
        with varying friction angles and cube properties.
    """
    # Set the random seed for reproducibility
    random.seed(404)

    # Load the original input data file (inputs_2d.json or similar)
    with open(cfg.input_path, 'r') as file:
        data = json.load(file)

    # Check if the output directory exists, if not, create it
    if not os.path.exists(cfg.output_path):
        os.makedirs(cfg.output_path)

    # If random velocity is enabled, adjust the number of files to generate
    if cfg.init_state.random_velocity:
        # Divide the number of files by 2 if random velocity is enabled
        n_files = int(cfg.friction_angle.n_files / 2)
        cfg.friction_angle.n_files = n_files

    # Create the JSON files with varying angles and cube properties
    create_files(data, cfg)


if __name__ == "__main__":
    main()
