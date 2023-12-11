from opcua import Client
import time
import paho.mqtt.client as mqtt

opc_server_url = "opc.tcp://192.168.0.216:4840/freeopcua/server/"
temperature_node_path = "ns=2;i=1"
humidity_node_path = "ns=2;i=2"
slaveId_node_path = "ns=2;i=3"
funcion_node_path = "ns=2;i=4"
registroInit_node_path = "ns=2;i=5"

MQTT_BROKER_HOST = "broker.mqtt-dashboard.com"
MQTT_BROKER_PORT = 1883
MQTT_TEMPERATURE_TOPIC = "pi400/dhtReadmqttdata/temperature"
MQTT_HUMIDITY_TOPIC = "pi400/dhtReadmqttdata/humidity"
MQTT_SLAVEID_TOPIC = "pi400/dhtReadmqttdata/slaveId"
MQTT_FUNCION_TOPIC = "pi400/dhtReadmqttdata/funcion"
MQTT_REGISTROINIT_TOPIC = "pi400/dhtReadmqttdata/ragistroInit"

def on_publish(client, userdata, mid):
    print("Mensaje publicado con éxito")
    
def on_connect(client, userdata, flags, rc):
    print("Conectado al broker MQTT con código de resultado " + str(rc))

mqtt_client = mqtt.Client()
mqtt_client.on_publish = on_publish
mqtt_client.on_connect = on_connect

client = Client(opc_server_url)
client.connect()

try:
    mqtt_client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 60)
    mqtt_client.loop_start()
    while True:
        temperature = client.get_node(temperature_node_path).get_value()
        humidity = client.get_node(humidity_node_path).get_value()
        slaveId = client.get_node(slaveId_node_path).get_value()
        funcion = client.get_node(funcion_node_path).get_value()
        registroInit = client.get_node(registroInit_node_path).get_value()
        
        slaveId_payload = f"{slaveId}"
        mqtt_client.publish(MQTT_SLAVEID_TOPIC, slaveId_payload, qos=2)
        print("Publicando Esclavo ID:", slaveId_payload)
        
        funcion_payload = f"{funcion}"
        mqtt_client.publish(MQTT_FUNCION_TOPIC, funcion_payload, qos=2)
        print("Publicando Funcion:", funcion_payload)
        
        registroInit_payload = f"{registroInit}"
        mqtt_client.publish(MQTT_REGISTROINIT_TOPIC, registroInit_payload, qos=2)
        print("Publicando Registro inicial:", registroInit_payload)

        temperature_payload = f"{temperature}"
        mqtt_client.publish(MQTT_TEMPERATURE_TOPIC, temperature_payload, qos=2)
        print("Publicando temperatura:", temperature_payload)
        
        humidity_payload = f"{humidity}"
        mqtt_client.publish(MQTT_HUMIDITY_TOPIC, humidity_payload, qos=2)
        print("Publicando humedad:", humidity_payload)

        time.sleep(5)

except KeyboardInterrupt:
    print("Programa interrumpido por el usuario")

finally:
    client.disconnect()
    mqtt_client.disconnect()
