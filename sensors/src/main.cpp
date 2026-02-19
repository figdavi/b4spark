// https://vimalb.github.io/IoT-ESP8266-Starter/Lesson_04/lesson.html

#include <Arduino.h>
#include "secrets.h" // **Edit "secrets.example.h" variables and rename to "secrets.h"**


#include <ESP8266WiFi.h>
WiFiClient WIFI_CLIENT;

#include <PubSubClient.h>
PubSubClient MQTT_CLIENT;

String deviceId = "esp8228_" + String(ESP.getChipId());

// Function declarations
void mqttReconnect();
void wifiReconnect();

void setup()
{
    Serial.begin(115200);

    // WiFi
    WiFi.begin(WIFI_SSID, WIFI_PASS);
    wifiReconnect();

    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());

    // MQTT
    // https://github.com/mqtt/mqtt.org/wiki/public_brokers
    MQTT_CLIENT.setServer("broker.hivemq.com", 1883);
    MQTT_CLIENT.setClient(WIFI_CLIENT);
}

void loop()
{
    if (!MQTT_CLIENT.connected())
    {
        mqttReconnect();
    }
    MQTT_CLIENT.loop();

    char topic[] = "mqtt_iot_123321/from_esp8266";
    String message = "Hello world! from" + deviceId;

    MQTT_CLIENT.publish(topic, message.c_str());
    Serial.println("Published!");

    delay(5000);
}

void wifiReconnect()
{
    Serial.println("Attempt to connect to WiFi");
    while (!WiFi.isConnected())
    {
        delay(3000);
        Serial.print(".");
    }
    Serial.println("WiFi connected");
}

void mqttReconnect()
{
    Serial.println("Attempt to connect to MQTT broker");
    while (!MQTT_CLIENT.connected())
    {
        MQTT_CLIENT.connect(deviceId.c_str());
        delay(3000);
        Serial.print(".");
    }

    Serial.println("MQTT connected");
}