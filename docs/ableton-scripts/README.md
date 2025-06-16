# Ableton Live Data Export Script

This project contains a Python script that interacts with the Ableton Live API to extract data from your Ableton Live set. The script is designed to be used as a MIDI Remote Script in Ableton Live.

## File Locations

- **Script Location:**  
  Place the entire script folder (e.g., `DataExportScript`) in the Ableton Live Remote Scripts directory.

  - **Windows:**  
    `C:\ProgramData\Ableton\Live 12 Suite\Resources\MIDI Remote Scripts\DataExportScript\`

  - **Mac:**  
    `~/Library/Preferences/Ableton/Live [version]/Remote Scripts/DataExportScript/`

- **Script Structure:**  
  Your script folder should contain at least:
  ```
  DataExportScript/
    __init__.py
    DataExportScript.py
    __pycache__/
  ```

## Compiling Python Files

1. Open a terminal in the root of this repository.
2. Run the following command to compile the scripts:
   ```
   python compile_scripts.py
   ```
3. This will generate `.pyc` files in the `DataExportScript/__pycache__/` directory.

## Using the Script in Ableton Live

1. Copy the entire `DataExportScript` folder (including `__pycache__`) to the Ableton Remote Scripts directory as described above.
2. Restart Ableton Live.
3. In Ableton, go to **Preferences > MIDI** and select your script from the Control Surface dropdown.

## Data Extracted

- **Trigger Markers:** Cue points or locators in the arrangement view.
- **MIDI Patterns:** MIDI note data from clips.
- **Transient Markers:** Beat or slice points from audio clips.

The extracted data will be exported to a JSON file (e.g., `ableton_data.json`) for use in your web app.