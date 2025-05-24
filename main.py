from PIL import Image, ImageDraw, ImageFont
import os

def strings_to_images(string_list,
                      font_path, # Added font_path argument
                      output_folder="output_images",
                      image_size=(300, 400), # Default image size adjusted for 3:4
                      font_size=60, # Default font size adjusted
                      background_color="white",
                      text_color="black"):
    """
    Exports a list of strings to images of the same size.

    Args:
        string_list (list): A list of strings to be converted to images.
        font_path (str): Path to the .ttf or .otf font file.
        output_folder (str): The folder where images will be saved.
        image_size (tuple): A tuple (width, height) for the output images.
        font_size (int): The font size for the text.
        background_color (str): The background color of the images.
        text_color (str): The color of the text.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    try:
        font = ImageFont.truetype(font_path, font_size)
        print(f"Successfully loaded font: {font_path}")
    except IOError:
        print(f"Error: Font file not found at '{font_path}'.")
        print("Please provide a correct path to a .ttf or .otf font file.")
        print("Falling back to default font, which may cause issues with text rendering and positioning.")
        # Fallback to default font - textbbox will likely fail here as you saw
        # For robust error handling, you might want to exit or raise an exception
        # if a proper font is critical (which it is for textbbox).
        try:
            font = ImageFont.load_default()
        except Exception as e:
            print(f"Could not load default font either: {e}")
            return # Exit if no font can be loaded

    for i, text_content in enumerate(string_list):
        img = Image.new('RGB', image_size, color=background_color)
        draw = ImageDraw.Draw(img)

        try:
            # Calculate text position (centered)
            # For Pillow versions 9.2.0 and later, use getbbox
            text_bbox = draw.textbbox((0, 0), text_content, font=font)
            text_width = text_bbox [2] - text_bbox [0]
            text_height = text_bbox [3] - text_bbox [1]
        except ValueError as e:
            # This error occurs if a non-TrueType font is used with textbbox
            print(f"ValueError with textbbox: {e}. This usually means the loaded font is not a TrueType/OpenType font.")
            print("Attempting to use textlength (Pillow 10+) or textsize (older Pillow) as a fallback for width, height might be less accurate.")
            # Fallback for text dimensions if textbbox fails (less accurate for height without TrueType)
            try: # Pillow 10+
                text_width = draw.textlength(text_content, font=font)
            except AttributeError: # Older Pillow
                 # textsize is deprecated but might exist
                try:
                    text_width, text_height_fallback = draw.textsize(text_content, font=font)
                except AttributeError:
                    print("Cannot determine text dimensions with the current font. Skipping text centering for this image.")
                    text_width = image_size [0] / 2 # Arbitrary, won't center
                    text_height_fallback = font_size # Rough estimate
            # For height with default font, it's harder to get accurately without TrueType info.
            # We might just use font_size or a fixed proportion.
            # This part becomes tricky if textbbox fails due to a non-TrueType font.
            # The best solution is to ensure a TrueType font IS loaded.
            text_height = font_size * 1.2 # A rough approximation

            if not isinstance(font, ImageFont.FreeTypeFont): # Check if it's not a TrueType/OpenType font
                 print("********************************************************************************")
                 print("WARNING: The loaded font is NOT a TrueType/OpenType font.")
                 print("Text centering and accurate sizing will be compromised.")
                 print("PLEASE PROVIDE A VALID .TTF or .OTF FONT FILE via the 'font_path' argument.")
                 print("********************************************************************************")
                 # If the font is not TrueType, text_bbox will fail.
                 # We must avoid using text_bbox and accept less accurate centering.
                 # For this example, we'll proceed with potentially poor centering if font is not TrueType.
                 # In a real application, you might want to stop execution or handle this more strictly.


        x = (image_size [0] - text_width) / 2
        # Move the text slightly closer to the top
        y = ((image_size [1] - text_height) / 2) * 0.6 # Adjust 0.8 as needed

        draw.text((x, y), text_content, font=font, fill=text_color)

        try:
            img.save(os.path.join(output_folder, f"{text_content}.png"))
            print(f"Saved image_{i+1}.png")
        except Exception as e:
            print(f"Error saving {text_content}.png: {e}")


def get_syllables():
    vowels = ['a', 'e', 'i', 'o', 'u']
    single_consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'l', 'm', 'n', 'ñ', 'p', 'q', 'r', 's', 't', 'v', 'x', 'z']
    syllabes = vowels[:]

    for c in single_consonants:
        for v in vowels:
            syllabe = c + v
            if syllabe.startswith('q'):
                if not (syllabe.endswith('e') or syllabe.endswith('i')):
                    continue
                else:
                    syllabe = syllabe [0] + 'u' + syllabe [1]
            if syllabe [0] in ['h', 'x', 'w', 'y',]:
                continue
            syllabes.append(syllabe)

    syllabes.extend(c)
    syllabes.extend([str(i) for i in range(1, 10)])

    return syllabes


if __name__ == '__main__':
    my_strings = get_syllables()

    # ----- IMPORTANT: SET YOUR FONT PATH HERE -----
    # Option 1: Place a font file (e.g., "DejaVuSans.ttf") in the same directory as your script
    # font_file_path = "DejaVuSans.ttf" # Make sure DejaVuSans.ttf is in the same folder

    # Option 2: Provide the full path to a font file on your system
    # Example for Linux (replace with an actual font path on your system):
    font_file_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    # Example for Windows (replace with an actual font path on your system):
    # font_file_path = "C:/Windows/Fonts/arial.ttf"
    # Example for macOS (replace with an actual font path on your system):
    # font_file_path = "/Library/Fonts/Arial.ttf"

    # Check if the chosen font path exists BEFORE calling the function
    if not os.path.exists(font_file_path):
        print(f"CRITICAL ERROR: The font file '{font_file_path}' was not found.")
        print("Please verify the path and make sure the font file exists.")
        print("The script will likely fail or produce poor results without a valid font.")
        # You might want to exit here if the font is absolutely required
        # exit()

    output_directory = "my_text_images_truetype"

    # Invert the aspect ratio: now 3:4 (width:height)
    img_width = 300 # Example width
    img_height = int(img_width * 4 / 3) # Calculates height to maintain 3:4 aspect (300 * 4/3 = 400)

    # Duplicate the font size
    font_size = 150 # Original was 30, now 60

    bg_color = "lightgreen"
    txt_color = "darkgreen"

    strings_to_images(
        my_strings,
        font_path=font_file_path, # Pass the font path
        output_folder=output_directory,
        image_size=(img_width, img_height), # Updated image_size for 3:4 ratio
        font_size=font_size, # Duplicated font size
        background_color=bg_color,
        text_color=txt_color
    )

    print(f"\nImages saved in the '{output_directory}' folder.")