import sys
import time
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!")


def cpu_temp():
    with open("/sys/class/thermal/thermal_zone0/temp", 'r') as f:
        return float(f.read())/1000


def main():
    channel = 7
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

    # close air fan first
    GPIO.setup(channel, GPIO.OUT, initial=GPIO.HIGH)
    is_close = True
    while True:
        temp = cpu_temp()
        if is_close:
            if temp > 20.0:
                print time.ctime(), temp, 'open air fan'
                GPIO.output(channel, GPIO.HIGH)
                is_close = False
        else:
            if temp < 15.0:
                print time.ctime(), temp, 'close air fan'
                GPIO.output(channel, GPIO.LOW)
                is_close = True

        time.sleep(2.0)
        print time.ctime(), temp


if __name__ == '__main__':
    main()
