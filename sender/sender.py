import time
import spidev
import RPi.GPIO as GPIO
from lib_nrf24 import NRF24

GPIO.setmode(GPIO.BCM)

PIPES = [[0x31, 0x4e, 0x6f, 0x64, 0x65], [0x32, 0x4e, 0x6f, 0x64, 0x65]]
MESSAGE_SIZE = 8

# INIT START
radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0, 17)

radio.setDataRate(NRF24.BR_250KBPS)
radio.setPayloadSize(MESSAGE_SIZE)
radio.setCRCLength(NRF24.CRC_8)
radio.setPALevel(NRF24.PA_LOW)

# REVERSE AS ARDUINO RECIEVER
radio.openWritingPipe(PIPES[1])
radio.openReadingPipe(1, PIPES[0])

radio.startListening()
radio.printDetails()
# INIT DONE


def formatMessage(message):
    data = list(message)
    data += '\0' * (MESSAGE_SIZE - len(data))
    return data


def main():
    while True:
        mess = input("Please type your message : ")[:MESSAGE_SIZE]
        radio.stopListening()

        dd = radio.write(formatMessage(mess))
        print("Sent the messgae {}, {}".format(mess, dd))

        time.sleep(1)

        radio.startListening()


try:
    main()
except KeyboardInterrupt:
    GPIO.cleanup()
