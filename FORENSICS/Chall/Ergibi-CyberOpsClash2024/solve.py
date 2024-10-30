from PIL import Image
import re


def hex_to_rgb(hex_color):
    """
    Convert a hexadecimal color to an RGB tuple.

    :param hex_color: Hexadecimal color string (e.g., '#060805FF').
    :return: Tuple of RGB values (R, G, B).
    """
    hex_color = hex_color.lstrip("#")  # Remove the '#' if present
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return (r, g, b)


def create_image_from_file(file_path, width, height, output_file):
    """
    Create an image from a file containing coordinates and RGB values.

    :param file_path: Path to the file with coordinates and RGB values.
    :param width: Width of the image.
    :param height: Height of the image.
    :param output_file: Path to save the output image.
    """
    # Create a new image with the given width and height
    image = Image.new("RGB", (width, height), color=(0, 0, 0))

    # Get the pixel map of the image
    pixels = image.load()

    # Read the file and process each line
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            # Use regular expression to extract coordinates and color
            match = re.match(r"\((\d+), (\d+), (#\w{8})\)", line)
            if match:
                x, y, hex_color = match.groups()
                x = int(x)
                y = int(y)
                rgb = hex_to_rgb(hex_color)
                if 0 <= x < width and 0 <= y < height:
                    pixels[x, y] = rgb
            else:
                print(f"Skipping invalid line: {line}")

    # Save the image
    image.save(output_file)
    print(f"Image saved as {output_file}")


if __name__ == "__main__":
    # Define the path to the input file
    file_path = "ergibi.txt"

    # Define the dimensions of the image
    width = 1000  # Adjust according to your needs
    height = 400  # Adjust according to your needs

    # Define the output file path
    output_file = "output_image.png"

    # Create the image
    create_image_from_file(file_path, width, height, output_file)
