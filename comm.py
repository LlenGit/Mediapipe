import serial
import time

# Set up serial communication with Arduino
arduino = serial.Serial(port='COM11', baudrate=9600, timeout=.1)  # Update 'port' to your correct port

def send_command(command):
    arduino.write(bytes(command + '\n', 'utf-8'))
    time.sleep(0.05)
    response = arduino.readline()
    return response.decode('utf-8').strip()

# Example: Move the index finger to 90 degrees and thumb to 45 degrees
response_index = send_command('INDEX 90')
print(response_index)

response_thumb = send_command('THUMB 45')
print(response_thumb)
