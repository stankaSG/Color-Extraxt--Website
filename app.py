from colorthief import ColorThief
from colormap import rgb2hex
from flask import Flask, render_template, url_for, request, redirect
import os
from flask_bootstrap import Bootstrap5

app = Flask(__name__)
Bootstrap5(app)

palette_img = "static/assets/image.jpg"
UPLOADS = "static/assets/uploads"

app.config['UPLOAD_FOLDER'] = UPLOADS


def extract_colors_from_img(img):
    color_thief = ColorThief(img)
    palette = color_thief.get_palette(color_count=10, quality=1)
    hex_palette = [rgb2hex(r, g, b) for r, g, b in palette]

    return hex_palette


@app.route('/')
def home():


    return render_template("index.html")

@app.route("/upload", methods=["GET", 'POST'])
def upload_img():
    if 'image' not in request.files:
        return redirect(url_for("home"))

    file = request.files['image']
    if file.filename == '':
        return redirect(url_for("home"))
    if file:
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        palette = extract_colors_from_img(filepath)

        return render_template("index.html", palette=palette, img_path=filepath, _anchor="upload-img")





    pass


if __name__ == "__main__":
    # Get the PORT from environment variable, default to 5000 if not set
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
