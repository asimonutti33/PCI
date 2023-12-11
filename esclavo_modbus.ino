#include <DHT.h>

#define DHTPIN 2        // Pin de datos del sensor DHT11
#define DHTTYPE DHT11   // Tipo de sensor DHT

#define timeOut 2000

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  if (Serial.available() > 0) {
    unsigned long startTime = millis();
    while (Serial.available() < 8 && (millis() - startTime) < timeOut) {
      //delay();
    }

    // Leer el mensaje Modbus
    byte message[8];
    for (int i = 0; i < 8; i++) {
      message[i] = Serial.read();
    }

    // Verificar dirección y función Modbus
    if (message[0] == 0x01 && message[1] == 0x03) {  // Dirección 1 y función 3 (lectura analógica)
      int registerAddress = (message[2] << 8) | message[3];
      int registerCount = (message[4] << 8) | message[5];

      // Leer datos del DHT11
      float humidity = dht.readHumidity();
      float temperature = dht.readTemperature();

      int humInt = humidity * 10;
      int temInt = temperature * 10;

      int slaveId = message[0];

      // Responder con datos del DHT11 en formato Modbus
      byte response[] = {
        slaveId,
        0x03,
        registerCount * 2,
        highByte(humInt),
        lowByte(humInt),
        highByte(temInt),
        lowByte(temInt),
      };
      int crc = calculateCRC(response, 7);
      response[7] = lowByte(crc);
      response[8] = highByte(crc);
      Serial.write(response, 9);
      //delay(2000);
    }
  }
}

int calculateCRC(byte* buf, int len) {
  unsigned int crc = 0xFFFF;

  for (int pos = 0; pos < len; pos++) {
    crc ^= (unsigned int)buf[pos];          // XOR byte into least sig. byte of crc

    for (int i = 8; i != 0; i--) {          // Loop over each bit
      if ((crc & 0x0001) != 0) {            // If the LSB is set
        crc >>= 1;                         // Shift right and XOR 0xA001
        crc ^= 0xA001;
      } else {                             // Else LSB is not set
        crc >>= 1;                         // Just shift right
      }
    }
  }
  // Note, this number has low and high bytes swapped, so use it accordingly (or swap bytes)
  return crc;
  //Serial.println(crc);
}

