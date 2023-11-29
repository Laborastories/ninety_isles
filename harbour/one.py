import sys
import cv2
from PIL import Image
import numpy as np
import ST7735
import time


def pil_image_to_opencv(pil_image):
    return cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)


if len(sys.argv) > 1:
    image_file = sys.argv[1]
else:
    print(f"Usage: {sys.argv[0]} <filename.gif>")
    sys.exit(0)

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
frame = 0

while True:
    try:
        # Convert PIL image to OpenCV format
        cv_image = pil_image_to_opencv(image)
        cv_image = cv2.resize(cv_image, (160, 80))

        # Display the frame
        # cv2.imshow("Frame", cv_image)
        disp.display(cv_image)
        if cv2.waitKey(10) & 0xFF == ord("q"):
            break

        # Go to the next frame of the GIF
        image.seek(image.tell() + 1)
        time.sleep(0.01)

    except EOFError:
        # Restart the GIF from the beginning
        image.seek(0)
