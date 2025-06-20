from io import BytesIO
from flask import Flask, render_template, request, send_file
from PIL import Image

TARGET_SIZE = (800, 800)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    files = request.files.getlist('images')
    frames = []
    for f in files:
        if f.filename:
            img = Image.open(f.stream).convert('RGBA')
            img.thumbnail(TARGET_SIZE, Image.LANCZOS)
            frame = Image.new('RGBA', TARGET_SIZE, (255, 255, 255, 0))
            frame.paste(img, ((TARGET_SIZE[0] - img.width) // 2,
                              (TARGET_SIZE[1] - img.height) // 2))
            frames.append(frame)
    if not frames:
        return 'No images uploaded', 400
    gif_bytes = BytesIO()
    frames[0].save(
        gif_bytes,
        format='GIF',
        save_all=True,
        append_images=frames[1:],
        duration=300,
        loop=0,
        disposal=2
    )
    gif_bytes.seek(0)
    return send_file(
        gif_bytes,
        mimetype='image/gif',
        as_attachment=False
    )

if __name__ == '__main__':
    app.run(debug=True)
