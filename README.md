# random

This repository contains experiments. Included is a small Flask application
that can generate a GIF from uploaded images. The resulting animation is
always 800&times;800 pixels by default, with each frame resized to fit without
distortion. A slider allows you to pick the maximum file size in megabytes;
the server will try to scale the frames to keep the GIF under that limit.

The HTML template now uses [Tailwind CSS](https://tailwindcss.com/) via CDN to
provide basic styling and includes icons from
[Heroicons](https://heroicons.com/) and
[Lucide](https://lucide.dev/) loaded via CDN.

## Running the GIF generator

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start the application:
   ```bash
   python gif_app/app.py
   ```

3. Open your browser at [http://localhost:5000](http://localhost:5000)
and upload images to receive the generated GIF.
