import os

def get_first_image_path(subfolder_name, root_folder):
    subfolder_path = os.path.join(root_folder, subfolder_name)

    if os.path.exists(subfolder_path):
        for file in os.listdir(subfolder_path):
            file_path = os.path.join(subfolder_path, file)
            if os.path.isfile(file_path):
                return file_path

    return None

# Example usage:
subfolder_name = '1'  # Replace with the subfolder name you want to access
root_folder = 'training_data'  # Replace with the actual path to your images folder
image_path = get_first_image_path(subfolder_name, root_folder)
print(image_path)
if image_path:
    print(f"First image path in subfolder {subfolder_name}: {image_path}")
else:
    print(f"No image found in subfolder {subfolder_name}")
