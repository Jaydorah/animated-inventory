from PIL import Image, ImageSequence
import numpy as np
import os
import shutil


def extract_gif_frames(gif_path, target_size=(176, 166)):
    frames = []
    with Image.open(gif_path) as gif:
        for frame in ImageSequence.Iterator(gif):
            frame_rgba = frame.convert('RGBA')
            resized_frame = frame_rgba.resize(
                target_size, Image.Resampling.LANCZOS)
            frames.append(resized_frame)

    print(f"Extracted {len(frames)} frames from GIF")
    return frames


def is_green_pixel(pixel, tolerance=10):
    r, g, b = pixel[0], pixel[1], pixel[2]
    return g > r + tolerance and g > b + tolerance


def find_green_bounding_box(inventory_img):
    inv_array = np.array(inventory_img.convert('RGBA'))

    min_x, min_y = float('inf'), float('inf')
    max_x, max_y = -1, -1

    for y in range(inv_array.shape[0]):
        for x in range(inv_array.shape[1]):
            pixel = inv_array[y, x]
            if is_green_pixel(pixel):
                min_x = min(min_x, x)
                min_y = min(min_y, y)
                max_x = max(max_x, x)
                max_y = max(max_y, y)

    if max_x == -1:
        return None

    return (min_x, min_y, max_x, max_y)


def replace_green_pixels(inventory_img, gif_frame):
    inv_rgba = inventory_img.convert('RGBA')
    green_bbox = find_green_bounding_box(inv_rgba)

    if green_bbox is None:
        print("Warning: No green pixels found in inventory!")
        return inv_rgba

    min_x, min_y, max_x, max_y = green_bbox
    print(f"Green pixel area found: ({min_x}, {min_y}) to ({max_x}, {max_y})")

    inv_array = np.array(inv_rgba)
    gif_array = np.array(gif_frame)

    result_array = inv_array.copy()

    inv_height, inv_width = inv_array.shape[0], inv_array.shape[1]
    gif_height, gif_width = gif_array.shape[0], gif_array.shape[1]

    offset_x = min_x
    offset_y = min_y

    print(f"Placing GIF at offset: ({offset_x}, {offset_y})")

    for y in range(inv_height):
        for x in range(inv_width):
            pixel = inv_array[y, x]
            if is_green_pixel(pixel):
                gif_x = x - offset_x
                gif_y = y - offset_y

                if 0 <= gif_x < gif_width and 0 <= gif_y < gif_height:
                    result_array[y, x] = gif_array[gif_y, gif_x]

    return Image.fromarray(result_array, 'RGBA')


def create_vertical_stack(frames, inventory_width, inventory_height):
    num_frames = len(frames)
    total_height = inventory_height * num_frames

    stacked_image = Image.new('RGBA', (inventory_width, total_height))

    for i, frame in enumerate(frames):
        y_position = i * inventory_height
        stacked_image.paste(frame, (0, y_position))
        print(f"Pasted frame {i+1} at y={y_position}")

    return stacked_image


def main():
    inventory_path = "inventory.png"
    gif_path = "input.gif"
    assets_source = "assets"
    done_folder = "done"

    print("Starting process...")

    print("1. Extracting GIF frames...")
    gif_frames = extract_gif_frames(gif_path, target_size=(176, 166))

    print("2. Loading inventory image...")
    inventory = Image.open(inventory_path)
    inv_width, inv_height = inventory.size
    print(f"Inventory size: {inv_width}x{inv_height}")

    print("3. Replacing green pixels for each frame...")
    processed_frames = []
    for i, gif_frame in enumerate(gif_frames):
        print(f"Processing frame {i+1}/{len(gif_frames)}...")
        processed_frame = replace_green_pixels(inventory, gif_frame)
        processed_frames.append(processed_frame)

    print("4. Creating vertical stack...")
    final_image = create_vertical_stack(
        processed_frames, inv_width, inv_height)

    print("5. Setting up output directories...")

    if os.path.exists(done_folder):
        print(f"Removing existing '{done_folder}' folder...")
        shutil.rmtree(done_folder)

    os.makedirs(done_folder)

    print(f"Copying '{assets_source}' to '{done_folder}/assets'...")
    shutil.copytree(assets_source, os.path.join(done_folder, "assets"))

    print("6. Saving output files...")

    anim_dir = os.path.join(done_folder, "assets",
                            "minecraft", "mcpatcher", "anim")
    os.makedirs(anim_dir, exist_ok=True)
    anim_output_path = os.path.join(anim_dir, "anim.png")

    inventory_dir = os.path.join(
        done_folder, "assets", "minecraft", "textures", "gui", "container")
    os.makedirs(inventory_dir, exist_ok=True)
    inventory_output_path = os.path.join(inventory_dir, "inventory.png")

    print(f"Saving stacked animation to {anim_output_path}...")
    final_image.save(anim_output_path, 'PNG')

    print(f"Saving first frame to {inventory_output_path}...")
    processed_frames[0].save(inventory_output_path, 'PNG')

    print(f"Files saved:")
    print(f"  Animation: {anim_output_path}")
    print(f"  Inventory texture: {inventory_output_path}")
    print(f"  Final image size: {final_image.size[0]}x{final_image.size[1]}")
    print(f"  Number of frames: {len(processed_frames)}")
    print(f"done copy assets from {os.path.join(done_folder, 'assets')}!")


if __name__ == "__main__":
    main()
