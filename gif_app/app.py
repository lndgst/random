from io import BytesIO
from flask import Flask, render_template, request, send_file
from PIL import Image

TARGET_SIZE = (800, 800)
DEFAULT_MAX_MB = 4

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    files = request.files.getlist('images')
    duration = int(request.form.get('duration', 300))
    max_mb = int(request.form.get('max_size', DEFAULT_MAX_MB))
    max_bytes = max_mb * 1024 * 1024

    images = []
    for f in files:
        if f.filename:
            img = Image.open(f.stream).convert('RGBA')
            img.thumbnail(TARGET_SIZE, Image.LANCZOS)
            images.append(img)

    if not images:
        return 'No images uploaded', 400

    scale = 1.0
    gif_bytes = BytesIO()
    for _ in range(5):
        size = (int(TARGET_SIZE[0] * scale), int(TARGET_SIZE[1] * scale))
        frames = []
        for img in images:
            frame = Image.new('RGBA', size, (255, 255, 255, 0))
            temp = img.copy()
            temp.thumbnail(size, Image.LANCZOS)
            frame.paste(temp, ((size[0] - temp.width) // 2,
                              (size[1] - temp.height) // 2))
            frames.append(frame)
        gif_bytes.seek(0)
        gif_bytes.truncate()
        frames[0].save(
            gif_bytes,
            format='GIF',
            save_all=True,
            append_images=frames[1:],
            duration=duration,
            loop=0,
            disposal=2,
            optimize=True
        )
        if len(gif_bytes.getvalue()) <= max_bytes:
            break
        scale *= 0.9

    gif_bytes.seek(0)
    return send_file(
        gif_bytes,
        mimetype='image/gif',
        as_attachment=False
    )

if __name__ == '__main__':
    app.run(debug=True)
