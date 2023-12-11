import serial
from opcua import Server
import time

server = Server()
server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")
server.set_server_name("RaspberryPi OPC UA Server")

uri = "http://example.org"
idx = server.register_namespace(uri)
temp = server.nodes.objects.add_variable(idx, "Temperature", 0.0)
hum = server.nodes.objects.add_variable(idx, "Humidity", 0.0)
slave_id = server.nodes.objects.add_variable(idx, "Identificacion", 0)
funcion = server.nodes.objects.add_variable(idx, "Funcion", 0)
registroInit = server.nodes.objects.add_variable(idx, "Registro", 0)
temp.set_writable()
hum.set_writable()
slave_id.set_writable()
funcion.set_writable()
registroInit.set_writable()

server.start()
print("Servidor OPC UA iniciado en opc.tcp://0.0.0.0:4840/freeopcua/server/")

SLAVE_ID = 1
RESPONSE_TIMEOUT = 5  

def calculateCRC(buf):
    crc = 0xFFFF

    for byte in buf[:-2]:
        crc ^= byte

        for _ in range(8):
            if crc & 0x0001:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1

    return crc

def validate_response(response):
    if len(response) < 4:
        return False  

    crc_received = (response[8] << 8) | response[7]
    crc_calculated = calculateCRC(response)

    return crc_received == crc_calculated

def read_modbus_data(register_address, register_count):
    request = [
        SLAVE_ID,              
        0x03,                  
        (register_address >> 8) & 0xFF, register_address & 0xFF,  
        (register_count >> 8) & 0xFF, register_count & 0xFF,      
    ]

    crc = calculateCRC(request)
    request.extend([crc & 0xFF, (crc >> 8) & 0xFF])

    ser.write(bytearray(request))

    time.sleep(0.005)  
    response_length = 9
    start_time = time.time()

    while ser.in_waiting < response_length and (time.time() - start_time) < RESPONSE_TIMEOUT:
        pass

    response = ser.read(response_length)

    if validate_response(response):
        humidity = (response[3] << 8) | response[4]
        temperature = (response[5] << 8) | response[6]
        idValor = response[0]
        FuncValor = response[1]
        RegistroValor = (request[2] << 8) | request[3]
        
        temp.set_value(temperature / 10)
        hum.set_value(humidity / 10)
        slave_id.set_value(idValor)
        funcion.set_value(FuncValor)
        registroInit.set_value(RegistroValor)
        
        print(f'ID: {idValor}, Funcion: {FuncValor}, Registro inicial: {RegistroValor}, Humedad: {humidity / 10}, Temperatura: {temperature / 10}')
    else:
        print('Error en la respuesta Modbus RTU')

    time.sleep(5)  

ser = serial.Serial('/dev/ttyS0', 9600, timeout=2)

try:
    while True:
        register_address = 0
        register_count = 2
        read_modbus_data(register_address, register_count)

except KeyboardInterrupt:
    print("Programa interrumpido por el usuario")

finally:
    ser.close()
    server.stop()
print("Servidor OPC UA detenido")
