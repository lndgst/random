# random

This repository contains experiments. Included is a small Flask application
that can generate a GIF from uploaded images. The resulting animation by
default is 800&times;800 pixels, but you can now customize the dimensions in
the web interface. Each frame is resized to fit without distortion and the
color depth is automatically adjusted based on the chosen size.

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
