# Proyecto de Comunicación Industrial

## Descripción

Este proyecto se centra en la implementación y comprensión detallada de tres protocolos de comunicación industrial fundamentales: MODBUS, OPC UA y MQTT. A través de la simulación de la comunicación MODBUS, la transición a OPC UA y la integración con MQTT, se explor cómo estos protocolos pueden mejorar la conectividad y eficiencia en entornos industriales.
Se sensan los datos del sensor de temperatura, estos datos se envian vía Modbus a la rasperberry Pi400, este dipositivo actua como maestro ModBus y servidor OPC UA, en un tercer dispositvo, la información se recibe y se publica bajo MQTT para que los mismos puedan ser visualizados a travez de cualquier dispositivo que posea conexión a Internet.

## Requisitos Previos
-Sensor DHT11
- Raspberry Pi 400
- Raspberry Pi 3
- Arduino Uno
- Sensor de temperatura DHT11
- OPC UA Server (UAExpert)
- Broker MQTT: broker.hivemq.com
- Node-Red para visualización de datos MQTT

## Estructura del Repositorio

El repositorio está organizado en carpetas separadas para cada protocolo, detallando la implementación y configuración específica de cada uno.

## Instrucciones de Uso

### 1. MODBUS

- Configuración de la comunicación MODBUS utilizando los pines TX/RX.
- Ajustes y parámetros necesarios para la simulación.

### 2. OPC UA

- Transformación del maestro MODBUS en un servidor OPC UA.
- Configuración y ejecución del cliente OPC.

### 3. MQTT

- Configuración del cliente MQTT para el envío de datos al broker MQTT.
- Visualización de datos a través de Node-Red u otras herramientas.

## Estructura del Código Fuente

- `/modbus`: Código relacionado con la comunicación MODBUS.
- `/opcua`: Implementación del servidor OPC UA y configuración del cliente OPC.
- `/mqtt`: Código para la comunicación MQTT y visualización de datos.

