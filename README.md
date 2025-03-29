# League Queue Auto-Acceptor

A tool that automatically clicks the "Accept" button in League of Legends when a match is found.

### ⚠️ **Disclaimer: This tool may violate Riot's Terms of Service and could result in a ban. Use at your own risk.**

## Features

- Detects League queue pop-ups
- Human-like mouse movement and randomized delay (2–6s)
- Start/Stop toggle and log panel
- Supports custom button image for any screen resolution

## How to Use

1. Make sure you have **Python 3.10 or above** installed.
2. Clone this repo:
   ```bash
   git clone https://github.com/yourusername/league-queue-auto-acceptor.git
   cd league-queue-auto-acceptor
   ```
3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the program:
   ```
   python main.py
   ```

## Build Executable

1. Make sure you have **pyinstaller** installed. (Should be installed if you ran `pip install -r requirements.txt`)
2. Build the executable:
   ```bash
   pyinstaller --onefile --windowed main.py
   ```
   This builds a single .exe file under the `dist` directory. Navigate to the `dist` directory and run the **_main.exe_** file to start the program.
3. Make a copy of the accept button image and place it in the same directory as the executable.
   ```
   copy accept_button.png dist\
   ```

## Notes

The default accept button image is made for 1600x900 resolution.
If you're using a different resolution, upload your own screenshot of the accept button using the app.

## License

This project is [MIT](https://github.com/ryangandev/league-queue-acceptor/blob/main/LICENSE) licensed.
