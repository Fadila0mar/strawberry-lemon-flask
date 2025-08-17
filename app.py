from flask import Flask, render_template, request, redirect, url_for
from ultralytics import YOLO
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['RESULT_FOLDER'] = 'static/results'

# Ensure folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULT_FOLDER'], exist_ok=True)

# Load your YOLO model
model = YOLO("yolov8n.pt")

@app.route("/", methods=["GET", "POST"])
def index():
    result_image = None
    if request.method == "POST":
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Run YOLO prediction
            results = model.predict(filepath)
            result_path = os.path.join(app.config['RESULT_FOLDER'], filename)
            results[0].plot().save(result_path)
            result_image = result_path

    return render_template("index.html", result_image=result_image)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
