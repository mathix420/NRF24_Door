#include <SPI.h>
#include <RF24.h>
#include <printf.h>
#include <nRF24L01.h>

RF24 radio(9, 10);

const uint64_t pipes[2] = { 0x314e6f6465LL, 0x324e6f6465LL };

void setup() {
    Serial.begin(115200);
    printf_begin();

    radio.begin();
    radio.setPayloadSize(8);
    radio.setCRCLength(RF24_CRC_8);
    radio.setDataRate(RF24_250KBPS);
    radio.setPALevel(RF24_PA_LOW);

    // REVERSE AS RPI SENDER
    radio.openWritingPipe(pipes[0]);
    radio.openReadingPipe(1, pipes[1]);

    radio.startListening();
    radio.printDetails();
}

void loop() {
    char response[8];

    if (radio.available()) {
        Serial.println("RADIO IS AVAILABLE");
        while (radio.available()) {
            radio.read( &response, sizeof(response) );
        }
        radio.stopListening();
        radio.write( &response, sizeof(response) );
        radio.startListening();
        Serial.print("Sent response ");
        Serial.println(response);
    }
}
