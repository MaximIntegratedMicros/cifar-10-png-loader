import os
import sys
import serial
import ft4222
import ft4222.SPI as SPI
import ft4222.SPIMaster as SPIM
import PIL.Image as Image

# Start - Match these with MAX78000 application
SERIAL_BAUD = 115200
IMG_WIDTH   = 32
IMG_HEIGHT  = 32
# End

SERIAL_TOUT = 5     # Seconds
IMG_MODE    = "RGB"

serial_dev = r'/dev/ttyUSB0'

def print_result(filename, result):
    print("{0}\t{1}".format(filename, result), end='')


def main():

    if len(sys.argv) < 2:
        print("ERROR Missing argument: path to test images")
        sys.exit()

    abs_path = os.path.realpath(sys.argv[1])
    if not os.path.exists(abs_path):
        print("ERROR Diretory does not exists: {0}".format(abs_path))
        sys.exit()

    print("\nTesting images from: {0}\n".format(abs_path))

    # Open device with default description
    MAX78000FTDI = ft4222.openByDescription('FT4222 A')

    MAX78000FTDI.spiMaster_Init(SPIM.Mode.SINGLE,
                                SPIM.Clock.DIV_8,
                                SPI.Cpol.IDLE_LOW,
                                SPI.Cpha.CLK_LEADING,
                                SPIM.SlaveSelect.SS0)

    # Serial port must be open before end of SPI transaction to avoid missing characters
    MAX78000Serial = serial.Serial(serial_dev, SERIAL_BAUD, timeout=SERIAL_TOUT)

    for filename in sorted(os.listdir(abs_path)):
        # Ignore all other files
        if not filename.endswith('.png'):
            continue

        with Image.open(os.path.join(abs_path, filename)) as img:
            if not img.mode == IMG_MODE:
                print_result(filename, "Skipped, image mode must be {0}\n".format(IMG_MODE))
                continue

            if not img.size == (IMG_WIDTH, IMG_HEIGHT):
                print_result(filename, "Skipped, image size must be {0}x{1}\n".format(IMG_WIDTH, IMG_HEIGHT))
                continue

            image_data = img.getdata()

        # Convert list of tuples to flat list
        image_data = [color_value for pixel in image_data for color_value in pixel]

        # Send image to MAX78000 SPI slave
        sent_bytes = MAX78000FTDI.spiMaster_SingleWrite(bytes(image_data), True)

        # Wait for the test result
        # read() blocks until SERIAL_TOUT
        result = []
        while 1:
            char = MAX78000Serial.read(1)
            if char == b'':
                result = "Timeout"
                break
            result.append(char.decode('utf-8'))
            if char == b'\n':
                result = "".join(result)
                break

        print_result(filename, result)

    MAX78000Serial.close()
    MAX78000FTDI.close()


if __name__ == "__main__":
    main()