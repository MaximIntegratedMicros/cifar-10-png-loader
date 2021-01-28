import os
import sys
import serial
import ft4222
import ft4222.SPI as SPI
import ft4222.SPIMaster as SPIM
import PIL.Image as Image

# Serial device and baud rate for MAX78000
serial_dev = r'/dev/ttyUSB0'
serial_baud = 115200

def print_result(filename, result):
    print("{0} - {1}".format(filename, result))


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
                                SPIM.Clock.DIV_8, # Must match the SPI Clock on MAX78000
                                SPI.Cpol.IDLE_LOW,
                                SPI.Cpha.CLK_LEADING,
                                SPIM.SlaveSelect.SS0)

    # Serial port must be open before end of SPI transaction to avoid missing characters
    MAX78000Serial = serial.Serial(serial_dev, serial_baud, timeout=5)

    for filename in os.listdir(abs_path):
        # Ignore all other files
        if not filename.endswith('.png'):
            continue

        with Image.open(os.path.join(abs_path, filename)) as img:
            if not img.mode == 'RGB':
                print_result(filename, "Skipped, image type must be RGB\n")
                continue

            if not img.size == (32,32):
                print_result(filename, "Skipped, image size must be 32x32\n")
                continue

            image_data = img.getdata()

        # Convert list of tuples to flat list
        image_data = [color_value for pixel in image_data for color_value in pixel]

        # Send image to MAX78000 SPI slave
        sent_bytes = MAX78000FTDI.spiMaster_SingleWrite(bytes(image_data), True)

        # Wait for test result of image
        # read() blocks until timeout
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