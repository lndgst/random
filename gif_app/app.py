from io import BytesIO
from flask import Flask, render_template, request, send_file, make_response
from PIL import Image
import uuid

DEFAULT_DIMENSION = 600
DEFAULT_MAX_MB = 4

app = Flask(__name__)

# Store uploaded images in memory keyed by a session id
UPLOAD_STORE = {}


def get_sid():
    """Return a session id from the cookie or generate a new one."""
    sid = request.cookies.get('sid')
    if not sid:
        sid = str(uuid.uuid4())
    return sid


def store_image(file, target_size):
    """Load a single uploaded image and resize it before storing."""
    if not file or not file.filename:
        return None
    img = Image.open(file.stream).convert('RGBA')
    img.thumbnail(target_size, Image.LANCZOS)
    return img

@app.route('/', methods=['GET'])
def index():
    """Render the main page and ensure a session cookie exists."""
    sid = get_sid()
    resp = make_response(render_template('index.html'))
    if 'sid' not in request.cookies:
        resp.set_cookie('sid', sid)
    return resp


@app.route('/upload', methods=['POST'])
def upload():
    """Accept a single image and store it in memory for the session."""
    sid = get_sid()
    dimension = int(request.form.get('dimension', DEFAULT_DIMENSION))
    img = store_image(request.files.get('image'), (dimension, dimension))
    if img is None:
        return 'No image uploaded', 400
    UPLOAD_STORE.setdefault(sid, []).append(img)
    return ('', 204)


@app.route('/clear', methods=['POST'])
def clear():
    """Remove all stored images for the current session."""
    sid = get_sid()
    UPLOAD_STORE.pop(sid, None)
    return ('', 204)

@app.route('/generate', methods=['POST'])
def generate():
    sid = get_sid()
    images = UPLOAD_STORE.get(sid, [])
    duration = int(request.form.get('duration', 300))
    dimension = int(request.form.get('dimension', DEFAULT_DIMENSION))
    max_mb = int(request.form.get('max_size', DEFAULT_MAX_MB))
    cover = request.form.get('cover', '0') == '1'
    max_bytes = max_mb * 1024 * 1024
    target_size = (dimension, dimension)

    if not images:
        return 'No images uploaded', 400

    scale = 1.0
    gif_bytes = BytesIO()
    for _ in range(5):
        size = (int(target_size[0] * scale), int(target_size[1] * scale))
        frames = []
        for img in images:
            frame = Image.new('RGBA', size, (255, 255, 255, 0))
            temp = img.copy()
            if cover:
                ratio = max(size[0] / temp.width, size[1] / temp.height)
                new_size = (int(temp.width * ratio), int(temp.height * ratio))
                temp = temp.resize(new_size, Image.LANCZOS)
                left = (temp.width - size[0]) // 2
                top = (temp.height - size[1]) // 2
                temp = temp.crop((left, top, left + size[0], top + size[1]))
                frame.paste(temp, (0, 0))
            else:
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
