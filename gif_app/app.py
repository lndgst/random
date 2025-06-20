from io import BytesIO
from flask import Flask, render_template, request, send_file
from PIL import Image

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    files = request.files.getlist('images')
    images = []
    for f in files:
        if f.filename:
            img = Image.open(f.stream)
            images.append(img.convert('RGBA'))
    if not images:
        return 'No images uploaded', 400
    gif_bytes = BytesIO()
    images[0].save(
        gif_bytes,
        format='GIF',
        save_all=True,
        append_images=images[1:],
        duration=300,
        loop=0
    )
    gif_bytes.seek(0)
    return send_file(
        gif_bytes,
        mimetype='image/gif',
        as_attachment=False
    )

if __name__ == '__main__':
    app.run(debug=True)
