import arcade
import os

def count_files(path, prefix):
    count = 0

    try:
        files = os.listdir(path)
    except Exception as e:
        print(f"Exception when getting files: {e}")
        return count

    for file in files:
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path) and file.startswith(prefix):
            count += 1

    return count

def load_texture_pair_h(path):
    return [
        arcade.load_texture(path),
        arcade.load_texture(path).flip_horizontally()
    ]


