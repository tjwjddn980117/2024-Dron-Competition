import os
import shutil
import random

def augment_data(source_dir, target_dir, desired_count=100):
    # Ensure target directory exists
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    # Iterate over each class directory in the source directory
    for class_name in os.listdir(source_dir):
        class_source_path = os.path.join(source_dir, class_name)
        class_target_path = os.path.join(target_dir, class_name)

        # Ensure class directory exists in the target directory
        if not os.path.exists(class_target_path):
            os.makedirs(class_target_path)

        # List all files in the class directory
        files = os.listdir(class_source_path)
        
        # Calculate how many times we need to duplicate the existing files
        current_count = len(files)
        if current_count == 0:
            continue  # Skip if there are no files in the directory
        
        # Copy original files to the target directory
        for file in files:
            shutil.copy(os.path.join(class_source_path, file), os.path.join(class_target_path, file))

        # Duplicate files until the desired count is reached
        while current_count < desired_count:
            file_to_copy = random.choice(files)  # Randomly select a file to duplicate
            new_file_name = f"{current_count}_{file_to_copy}"
            shutil.copy(os.path.join(class_source_path, file_to_copy), os.path.join(class_target_path, new_file_name))
            current_count += 1

# Define the source and target directories
source_directory = 'C:\\Users\\Seo\\Desktop\\Gits\\2024_06_Dron_Competition\\Data'
target_directory = 'C:\\Users\\Seo\\Desktop\\Gits\\2024_06_Dron_Competition\\Data_Argu'

# Perform data augmentation
augment_data(source_directory, target_directory, desired_count=300)