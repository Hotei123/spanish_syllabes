import os
import csv
import genanki # Optional: For direct Anki deck creation

# --- Configuration ---
IMAGE_FOLDER = "my_text_images_truetype"  # Change this to the path of your image folder
OUTPUT_CSV_FILENAME = "anki_cards.csv"
ANKI_DECK_NAME = "My Image Deck"
ANKI_NOTE_MODEL_NAME = "Image Basic"
ANKI_NOTE_MODEL_ID = 1234567891 # A unique ID for your note model (can be any large integer)
ANKI_DECK_ID = 2345678912 # A unique ID for your deck

# --- Create the image folder if it doesn't exist (for testing purposes) ---
if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)
    print(f"Created folder: {IMAGE_FOLDER}")
    print("Please place your images inside this folder and run the script again.")
    print("Exiting now.")
    exit()

# --- Part 1: Generate the CSV file for Anki Import ---
print(f"Generating '{OUTPUT_CSV_FILENAME}' for Anki import...")
image_files = [f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'))]

if not image_files:
    print(f"No image files found in '{IMAGE_FOLDER}'. Please make sure your images are there.")
else:
    with open(OUTPUT_CSV_FILENAME, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        for img_file in sorted(image_files): # Sort for consistent order
            # Front of the card: HTML img tag pointing to the image file
            # Back of the card: The image filename itself (you can change this!)
            csv_writer.writerow([f'<img src="{img_file}">', img_file])
    print(f"CSV file '{OUTPUT_CSV_FILENAME}' created successfully.")
    print(f"Found {len(image_files)} image(s).")
    print("\n--- Instructions for Anki Import (Method 2) ---")
    print(f"1. Open Anki Desktop.")
    print(f"2. Go to 'Tools' > 'Open Media Folder'.")
    print(f"3. Copy ALL your images from the '{IMAGE_FOLDER}' folder into Anki's 'collection.media' folder.")
    print(f"   (If you copied them to a subfolder within 'collection.media', say 'my_subimages',")
    print(f"   you would need to adjust the CSV generation to: <img src=\"my_subimages/{img_file}\">)")
    print(f"4. Create a new deck if you haven't already (e.g., '{ANKI_DECK_NAME}').")
    print(f"5. Go to 'File' > 'Import...'.")
    print(f"6. Select the '{OUTPUT_CSV_FILENAME}' file.")
    print(f"7. In the import window:")
    print(f"   - **Type:** Choose 'Basic' (or create a new Note Type with 'Front' and 'Back' fields if needed).")
    print(f"   - **Deck:** Select your desired deck (e.g., '{ANKI_DECK_NAME}').")
    print(f"   - **Field Mapping:**")
    print(f"     - Map 'Field 1 of {OUTPUT_CSV_FILENAME}' to 'Front'.")
    print(f"     - Map 'Field 2 of {OUTPUT_CSV_FILENAME}' to 'Back'.")
    print(f"   - Make sure 'Allow HTML in fields' is CHECKED.")
    print(f"8. Click 'Import'.")


# --- Part 2: (Optional) Direct Anki Deck Creation using genanki ---
# This method is often more robust as it handles media embedding directly.
print("\n--- (Optional) Direct Anki Deck Creation using genanki ---")
print("Requires 'genanki' library: pip install genanki")

try:
    # Define your Anki Note Model (how your cards look)
    # This is a basic model with a Front and Back field.
    # You can customize the CSS for better styling in Anki.
    image_model = genanki.Model(
        ANKI_NOTE_MODEL_ID,
        ANKI_NOTE_MODEL_NAME,
        fields=[
            {'name': 'Front'},
            {'name': 'Back'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{Front}}',
                'afmt': '{{Front}}<hr id="answer">{{Back}}',
            },
        ],
        css="""
            .card {
                font-family: arial;
                font-size: 20px;
                text-align: center;
                color: black;
                background-color: white;
            }
            img {
                max-width: 100%; /* Ensures images fit within the card */
                max-height: 400px; /* Adjust as needed */
            }
        """
    )

    my_deck = genanki.Deck(
        ANKI_DECK_ID,
        ANKI_DECK_NAME
    )

    my_package = genanki.Package(my_deck)
    media_files = [] # List to store paths of media files to include

    for img_file in sorted(image_files):
        img_path = os.path.join(IMAGE_FOLDER, img_file)
        if os.path.exists(img_path):
            media_files.append(img_path) # Add full path to media
            # Create a note: Front has the image, Back has the filename (or other text)
            note = genanki.Note(
                model=image_model,
                fields=[f'<img src="{img_file}">', img_file]
            )
            my_deck.add_note(note)
        else:
            print(f"Warning: Image file not found: {img_path}. Skipping.")

    my_package.media_files = media_files
    output_apkg_filename = f"{ANKI_DECK_NAME}.apkg"
    my_package.write_to_file(output_apkg_filename)
    print(f"\nAnki deck '{output_apkg_filename}' created successfully using genanki!")
    print(f"To import into Anki: Just double-click the '{output_apkg_filename}' file.")

except ImportError:
    print("\nSkipping 'genanki' direct deck creation. Install it with 'pip install genanki' to use this feature.")
except Exception as e:
    print(f"\nAn error occurred during genanki deck creation: {e}")