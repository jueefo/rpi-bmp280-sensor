# Raspberry Pi Sensor Reader

Raspberry Pi Sensor Reader is a Python program that reads temperature and air pressure data from a BMP280 sensor and blinks an LED. You can customize the measurement interval and runtime using command-line parameters.
## Installation

1. Clone this Git repository to your Raspberry Pi device:

```bash
git clone https://github.com/jueefo/rpi-bmp280-sensor
```
2. Navigate to the project's root directory:
```bash
cd rpi-bmp280-sensor
```
Install the necessary dependencies using the requirements.txt file:
```bash
pip install -r requirements.txt
```

## Usage

Using the program is straightforward from the command line. You can customize the measurement interval and runtime as follows:
```bash
python bmp280_sensor_reader.py --interval 2 --runtime 60
```
- --interval specifies the measurement interval in seconds.
- --runtime specifies the runtime in seconds. Set it to 0 to run the program indefinitely.

The program measures temperature and air pressure at the specified intervals and blinks the LED during each measurement cycle.

## Troubleshooting

If you encounter issues with the program, consider the following:
- Ensure that the BMP280 sensor is correctly connected to the Raspberry Pi.
