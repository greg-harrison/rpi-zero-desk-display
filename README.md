This project is based on the fantastic work of [Frederick Vandenbosch](http://frederickvandenbosch.be)
- Check out their original [project here](http://frederickvandenbosch.be/?p=1365)

---

### Install
- Upload the files to the RPI
- Use Chrontab to set up a chronjob that runs Launcher.sh on Reboot:
    - `sudo chrontab -e` 
    - `@reboot sh /home/pi/launcher.sh`

### Usage
- Press one button to change the screen, press the other to interact with the current display

---

### Hardware
- Uses Adafruit_SSD1306 Library to send signals to a small 128x32px Monochrome OLED display 
    - [Adafruit PiOLED](https://www.adafruit.com/product/3527)

### Code
- `clear_display()` → Empties the display
- `set_font()` → Uses the same for all functions
    - Argument: font size in pixels
- `display_custom()` → Returns any given text at the center of the display
    - Argument: text to display
- `string_width()` → Given the Font and the String, this returns the length to display
    - Argument1: fonttype
    - Argument2: string
- `display_time()` → Retrieves the time from the Py library and returns it in varying formats
- `display_network()` → Retrieves IP, Netmask, Gateway and SSID and returns