# Media Metadata Studio (Termux)

## Install dependencies
```bash
pkg update -y
pkg install python exiftool ffmpeg -y
python -m pip install -r requirements.txt
```

## Run
```bash
python app.py
```
Open `http://127.0.0.1:5000` in the same phone's browser.

## Notes
- Local-only: binds to 127.0.0.1.
- Supports common image/video extensions; metadata cleaning depends on ExifTool and file format.
- Custom device profile is stored as a sidecar JSON file, not forged into camera metadata.
- AI indicators are metadata clues only, not a reliable AI detector.
- Original uploads are retained in `uploads/`; processed outputs are in `output/`.
- Keep the phone secure; uploaded files consume local storage.
