'''
적게 찍은 사진을 강제로 사진을 랜덤으로 복사해서 다른 폴더에 더해넣는다.  

source_dir (str) : 원본 디렉토리
target_dir (str) : 새롭게 강제로 복사하여 옮길 폴더. 
desired_count (int) : 각 클래스당 몇 개까지 사진을 복사할 지. 
'''

import os
import shutil
import random

# Define the source and target directories
source_directory = ' '
target_directory = ' '

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


# Perform data augmentation
augment_data(source_directory, target_directory, desired_count=300)