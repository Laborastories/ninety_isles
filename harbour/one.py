import sys
from PIL import Image
import ST7735
import time
import numpy as np

if len(sys.argv) > 1:
    image_file = sys.argv[1]
else:
    print(f"Usage: {sys.argv[0]} <filename.gif>")
    sys.exit(0)
try:
    # Create TFT LCD display class.
    disp = ST7735.ST7735(
        port=0,
        cs=ST7735.BG_SPI_CS_FRONT,  # BG_SPI_CS_BACK or BG_SPI_CS_FRONT. BG_SPI_CS_FRONT (eg: CE1) for Enviro Plus
        dc=9,  # "GPIO9" / "PIN21". "PIN21" for a Pi 5 with Enviro Plus
        backlight=35,  # "PIN18" for back BG slot, "PIN19" for front BG slot. "PIN32" for a Pi 5 with Enviro Plus
        rotation=90,
        spi_speed_hz=4000000,
    )

    image = Image.open(image_file)

    # Initialize display.
    disp.begin()

    width = disp.width
    height = disp.height

    while True:
        try:
            image.seek(image.tell())
            frame = image.resize((disp.width, disp.height), Image.LANCZOS)

            frame_rgb = frame.convert('RGB')

            disp.display(frame_rgb)

            time.sleep(image.info['duration'] / 1000.0)

            image.seek(image.tell() + 1)

        except EOFError:
            # Restart the GIF from the beginning
            image.seek(0)
except Exception as e:
    print("Except!")
    print(e)
