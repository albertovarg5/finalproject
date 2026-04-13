"""
Final Project - Image Effects Web Application

This Flask application allows a user to upload an image, choose an image
processing effect, and view the processed result in a web browser.

Implemented effects:
- Grayscale
- Blur
- Edge Detection
- Invert Colors

The program uses OpenCV for image processing and Flask for the web interface.
It is designed to run locally and inside Docker using the PORT environment
variable required by the project template.
"""

from flask import Flask, request, render_template_string
import os
import cv2
import socket

# Create the Flask application
app = Flask(__name__)

# Get the machine hostname so it can be displayed on the page
hostname = socket.gethostname()

# Define folders for uploaded and processed images
UPLOAD_FOLDER = "static/uploads"
OUTPUT_FOLDER = "static/outputs"

# Make sure the folders exist before the app runs
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# HTML page shown in the browser
HTML = """
<h2>Image Effects App</h2>
<p><i>host={{ hostname }}</i></p>

<form method="POST" action="/process" enctype="multipart/form-data">
    <label>Image:</label>
    <input type="file" name="file" required>

    <label>Effect:</label>
    <select name="effect">
        <option value="grayscale">Grayscale</option>
        <option value="blur">Blur</option>
        <option value="edge">Edge Detection</option>
        <option value="invert">Invert Colors</option>
    </select>

    <input type="submit" value="Run">
</form>

<hr>

{% if original and processed %}
<h3>Result (Effect: {{ effect }})</h3>

<div style="display:flex; gap:20px; align-items:flex-start; flex-wrap:wrap;">
    <div>
        <p><b>Original</b></p>
        <img src="{{ original }}" style="max-width:350px;">
    </div>

    <div>
        <p><b>Processed</b></p>
        <img src="{{ processed }}" style="max-width:350px;">
    </div>
</div>
{% endif %}
"""


def process_image(input_path, output_path, effect):
    """
    Read the uploaded image, apply the chosen effect,
    and save the processed image.

    Parameters:
        input_path (str): path to the uploaded image
        output_path (str): path where the processed image will be saved
        effect (str): selected image effect
    """
    # Load the image from disk
    img = cv2.imread(input_path)

    # If the image could not be read, stop processing
    if img is None:
        return None

    # Apply grayscale effect
    if effect == "grayscale":
        result = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply blur effect
    elif effect == "blur":
        result = cv2.GaussianBlur(img, (15, 15), 0)

    # Apply edge detection effect
    elif effect == "edge":
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        result = cv2.Canny(gray, 50, 150)

    # Apply invert colors effect
    elif effect == "invert":
        result = cv2.bitwise_not(img)

    # If no valid effect is selected, return original image
    else:
        result = img

    # Save the processed image
    cv2.imwrite(output_path, result)
    return output_path


@app.route("/")
def home():
    """
    Display the main page with the upload form.
    """
    return render_template_string(
        HTML,
        original=None,
        processed=None,
        effect=None,
        hostname=hostname
    )


@app.route("/process", methods=["POST"])
def process_route():
    """
    Receive the uploaded file and selected effect,
    process the image, and display the result.
    """
    # Get the uploaded file and selected effect from the form
    file = request.files.get("file")
    effect = request.form.get("effect", "grayscale")

    # Define paths for original and processed files
    input_path = os.path.join(UPLOAD_FOLDER, "original.jpg")
    output_path = os.path.join(OUTPUT_FOLDER, "output.jpg")

    # Save the uploaded image if a file was chosen
    if file and file.filename != "":
        file.save(input_path)
    else:
        return "No image uploaded."

    # Process the uploaded image
    process_image(input_path, output_path, effect)

    # Show original and processed image in the browser
    return render_template_string(
        HTML,
        original="/static/uploads/original.jpg",
        processed="/static/outputs/output.jpg",
        effect=effect,
        hostname=hostname
    )


if __name__ == "__main__":
    # Use the PORT environment variable for Docker/Render compatibility
    port = int(os.environ.get("PORT", 80))
    app.run(host="0.0.0.0", port=port)