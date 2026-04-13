# final project
#
# to build:   docker build -t app .
# to run:     docker run -p 80:80 app
# in browser: http://localhost

from flask import Flask, request, render_template_string
import os
import cv2
import socket

app = Flask(__name__)

hostname = socket.gethostname()

UPLOAD_FOLDER = "static/uploads"
OUTPUT_FOLDER = "static/outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

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
    img = cv2.imread(input_path)

    if img is None:
        return None

    if effect == "grayscale":
        result = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    elif effect == "blur":
        result = cv2.GaussianBlur(img, (15, 15), 0)

    elif effect == "edge":
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        result = cv2.Canny(gray, 50, 150)

    elif effect == "invert":
        result = cv2.bitwise_not(img)

    else:
        result = img

    cv2.imwrite(output_path, result)
    return output_path


@app.route("/")
def home():
    return render_template_string(
        HTML,
        original=None,
        processed=None,
        effect=None,
        hostname=hostname
    )


@app.route("/process", methods=["POST"])
def process_route():
    file = request.files.get("file")
    effect = request.form.get("effect", "grayscale")

    input_path = os.path.join(UPLOAD_FOLDER, "original.jpg")
    output_path = os.path.join(OUTPUT_FOLDER, "output.jpg")

    if file and file.filename != "":
        file.save(input_path)
    else:
        return "No image uploaded."

    process_image(input_path, output_path, effect)

    return render_template_string(
        HTML,
        original="/static/uploads/original.jpg",
        processed="/static/outputs/output.jpg",
        effect=effect,
        hostname=hostname
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 80))
    app.run(host="0.0.0.0", port=port)