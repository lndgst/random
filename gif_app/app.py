from io import BytesIO
from flask import Flask, render_template, request, send_file
from PIL import Image

DEFAULT_SIZE = (800, 800)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    files = request.files.getlist('images')
    duration = int(request.form.get('duration', 300))
    width = int(request.form.get('width', DEFAULT_SIZE[0]))
    height = int(request.form.get('height', DEFAULT_SIZE[1]))
    target_size = (width, height)
    frames = []
    for f in files:
        if f.filename:
            img = Image.open(f.stream).convert('RGBA')
            img.thumbnail(target_size, Image.LANCZOS)
            frame = Image.new('RGBA', target_size, (255, 255, 255, 0))
            frame.paste(img, ((target_size[0] - img.width) // 2,
                              (target_size[1] - img.height) // 2))
            frames.append(frame)
    if not frames:
        return 'No images uploaded', 400
    # determine color depth based on target size to keep reasonable file size
    reference_pixels = DEFAULT_SIZE[0] * DEFAULT_SIZE[1]
    target_pixels = width * height
    color_ratio = reference_pixels / target_pixels if target_pixels else 1
    colors = max(16, min(256, int(256 * color_ratio)))

    processed_frames = [f.convert('P', palette=Image.ADAPTIVE, colors=colors)
                        for f in frames]

    gif_bytes = BytesIO()
    processed_frames[0].save(
        gif_bytes,
        format='GIF',
        save_all=True,
        append_images=processed_frames[1:],
        duration=duration,
        loop=0,
        disposal=2,
        optimize=True
    )
    gif_bytes.seek(0)
    return send_file(
        gif_bytes,
        mimetype='image/gif',
        as_attachment=False
    )

if __name__ == '__main__':
    app.run(debug=True)
