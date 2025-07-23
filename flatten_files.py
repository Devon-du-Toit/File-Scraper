import os
import json
import shutil
from pathlib import Path

def load_config(config_path='config.json'):
    with open(config_path, 'r') as f:
        return json.load(f)

def collect_files(input_dirs, extensions):
    collected_files = []
    for input_dir in input_dirs:
        for root, _, files in os.walk(input_dir):
            for file in files:
                if any(file.lower().endswith(ext.lower()) for ext in extensions):
                    full_path = os.path.join(root, file)
                    collected_files.append(full_path)
    return collected_files

def copy_to_flat_output(files, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for i, file_path in enumerate(files):
        filename = Path(file_path).name
        # Avoid overwriting: prepend index if name collision
        output_path = os.path.join(output_dir, f"{i}_{filename}")
        shutil.copy2(file_path, output_path)
    print(f"Copied {len(files)} files to '{output_dir}'.")

def main():
    config = load_config()
    input_dirs = config.get("input_dirs", [])
    extensions = config.get("file_extensions", [])
    output_dir = config.get("output_dir", "output")

    found_files = collect_files(input_dirs, extensions)
    copy_to_flat_output(found_files, output_dir)

if __name__ == "__main__":
    main()
