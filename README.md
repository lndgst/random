# random

This repository contains experiments. Included is a small Flask application
that can generate a GIF from uploaded images.

The HTML template now uses [Tailwind CSS](https://tailwindcss.com/) via CDN to
provide basic styling.

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
