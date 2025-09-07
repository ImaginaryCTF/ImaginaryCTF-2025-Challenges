#lmao entire thing is ai written slop but it works

import sys
import os
import math
from PIL import Image, ImageOps

TILE_SIZE = 32
OUT_FILE = 'reconstructed_mosaic.png'
TILES_MAP_FILE = 'stegosaurus.txt'

def load_tile_mapping(tiles_file):
    try:
        with open(tiles_file, 'r') as f:
            content = f.read().strip()
            if not content:
                return []
            # Split by whitespace and add .png extension
            tile_names = [name.strip() + '.png' for name in content.split() if name.strip()]
            return tile_names
    except FileNotFoundError:
        print(f"ERROR: Could not find tiles mapping file '{tiles_file}'")
        return None
    except Exception as e:
        print(f"ERROR: Could not read tiles mapping file: {e}")
        return None

def process_tile_image(tile_path):
    """Process a single tile image to match the original processing"""
    try:
        img = Image.open(tile_path)
        img = ImageOps.exif_transpose(img)

        # tiles must be square, so get the largest square that fits inside the image
        w = img.size[0]
        h = img.size[1]
        min_dimension = min(w, h)
        w_crop = (w - min_dimension) / 2
        h_crop = (h - min_dimension) / 2
        img = img.crop((w_crop, h_crop, w - w_crop, h - h_crop))

        # Resize to tile size
        tile_img = img.resize((TILE_SIZE, TILE_SIZE), Image.LANCZOS)
        return tile_img.convert('RGB')
    except Exception as e:
        print(f"ERROR: Could not process tile '{tile_path}': {e}")
        return None

def find_tile_file(tile_name, tiles_directory):
    """Find the full path of a tile file by searching recursively"""
    for root, dirs, files in os.walk(tiles_directory):
        if tile_name in files:
            return os.path.join(root, tile_name)
    return None

def calculate_mosaic_dimensions(num_tiles):
    """Calculate the dimensions of the mosaic grid"""
    # Try to find the closest square root
    sqrt_tiles = math.sqrt(num_tiles)
    
    # Try different aspect ratios to find valid dimensions
    for width in range(int(sqrt_tiles), num_tiles + 1):
        if num_tiles % width == 0:
            height = num_tiles // width
            return width, height
    
    # Fallback: assume square and pad if necessary
    side = int(math.ceil(sqrt_tiles))
    return side, side

def reconstruct_mosaic(tile_names, tiles_directory):
    """Reconstruct the mosaic from the tile names and directory"""
    if not tile_names:
        print("ERROR: No tile names provided")
        return False
    
    print(f"Reconstructing mosaic from {len(tile_names)} tiles...")
    
    # Calculate mosaic dimensions
    width_tiles, height_tiles = calculate_mosaic_dimensions(len(tile_names))
    print(f"Mosaic dimensions: {width_tiles} x {height_tiles} tiles")
    print(f"Output image size: {width_tiles * TILE_SIZE} x {height_tiles * TILE_SIZE} pixels")
    
    # Create the output image
    mosaic_width = width_tiles * TILE_SIZE
    mosaic_height = height_tiles * TILE_SIZE
    mosaic_img = Image.new('RGB', (mosaic_width, mosaic_height))
    
    # Process each tile
    tiles_processed = 0
    for i, tile_name in enumerate(tile_names):
        if i >= width_tiles * height_tiles:
            break  # Don't exceed the calculated dimensions
            
        print(f'Processing tile {i+1:4d}/{len(tile_names):4d}: {tile_name:30.30}', 
              flush=True, end='\r')
        
        # Find the tile file
        tile_path = find_tile_file(tile_name, tiles_directory)
        if not tile_path:
            print(f"\nWARNING: Could not find tile file '{tile_name}', skipping...")
            continue
        
        # Process the tile
        tile_img = process_tile_image(tile_path)
        if not tile_img:
            print(f"\nWARNING: Could not process tile '{tile_name}', skipping...")
            continue
        
        # Calculate position in the mosaic
        x_pos = (i % width_tiles) * TILE_SIZE
        y_pos = (i // width_tiles) * TILE_SIZE
        
        # Paste the tile into the mosaic
        mosaic_img.paste(tile_img, (x_pos, y_pos))
        tiles_processed += 1
    
    print(f"\nProcessed {tiles_processed} tiles successfully")
    
    # Save the reconstructed mosaic
    try:
        mosaic_img.save(OUT_FILE, format='PNG')
        print(f"Reconstructed mosaic saved as '{OUT_FILE}'")
        return True
    except Exception as e:
        print(f"ERROR: Could not save mosaic: {e}")
        return False

def show_usage():
    print("Usage: python reconstruct_mosaic.py <tiles_directory> [tiles_mapping_file]")
    print("  tiles_directory: Directory containing the original tile images")
    print("  tiles_mapping_file: Path to tiles.txt file (default: tiles.txt)")
    print("")
    print("This program reconstructs a photomosaic from a tiles.txt mapping file")
    print("created by the original mosaic generator.")

def main():
    # Parse command line arguments
    if len(sys.argv) < 2:
        show_usage()
        return
    
    tiles_directory = sys.argv[1]
    tiles_file = sys.argv[2] if len(sys.argv) > 2 else TILES_MAP_FILE
    
    # Validate inputs
    if not os.path.isdir(tiles_directory):
        print(f"ERROR: Tiles directory '{tiles_directory}' does not exist")
        return
    
    if not os.path.isfile(tiles_file):
        print(f"ERROR: Tiles mapping file '{tiles_file}' does not exist")
        return
    
    # Load the tile mapping
    print(f"Loading tile mapping from '{tiles_file}'...")
    tile_names = load_tile_mapping(tiles_file)
    if tile_names is None:
        return
    
    if not tile_names:
        print("ERROR: No tiles found in mapping file")
        return
    
    print(f"Found {len(tile_names)} tiles in mapping")
    
    # Reconstruct the mosaic
    success = reconstruct_mosaic(tile_names, tiles_directory)
    
    if success:
        print("Reconstruction completed successfully!")
    else:
        print("Reconstruction failed!")

if __name__ == '__main__':
    main()