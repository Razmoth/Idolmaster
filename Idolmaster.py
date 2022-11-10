from pathlib import Path
from lz4.block import decompress

import argparse

def read_i32(file):
    return int.from_bytes(file.read(4), 'little')

def decompress_bundle_file(file):
    output = bytes()

    value = read_i32(file)
    if value != 100:
        return False

    decompressed_size = read_i32(file)
    compressed_size = read_i32(file)
    is_compressed = bool(read_i32(file))
    data = file.read(compressed_size)

    if is_compressed:
        output = decompress(data, decompressed_size)
    else:
        output = data
        
    return output

def parse_args():
    parser = argparse.ArgumentParser('Idolmaster')
    parser.add_argument('input_folder', type=Path, help='Path to folder with compressed files.')
    parser.add_argument('output_folder', type=Path, help='Path to folder to save decompressed files.')

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    
    input_folder =  args.input_folder
    output_folder =  args.output_folder
    for path in input_folder.iterdir():
        with path.open('rb') as file:
            data = decompress_bundle_file(file)
            if not data:
                continue
        
        new_path = Path(output_folder,path.relative_to(input_folder))
        if not new_path.parent.exists():
            new_path.parent.mkdir()

        with new_path.open('wb') as file:
            file.write(data)