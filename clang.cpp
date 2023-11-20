#include <WiFi.h>
#include <PubSubClient.h>
#include <HTTPClient.h>

// กำหนดข้อมูลการเชื่อมต่อ Wi-Fi
const char* ssid = "Poompoo";
const char* password = "nongwawa";

// กำหนดข้อมูลการเชื่อมต่อ MQTT
const char* mqttServer = "10.53.99.234"; // MQTT Broker IP
const int mqttPort = 1883;
const char* mqttUser = "poompoo123";
const char* mqttPassword = "poompoo123";

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  Serial.begin(115200);
  
  // เชื่อมต่อ Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
  
  // เชื่อมต่อ MQTT
  client.setServer(mqttServer, mqttPort);
  if (client.connect("ESP32Client", mqttUser, mqttPassword)) {
    Serial.println("Connected to MQTT Broker!");
  } else {
    Serial.println("Failed to connect to MQTT Broker.");
    return;
  }
}

void loop() {
  // ข้อมูลที่จะส่ง
  String data = "{\"message\": \"ตตต\"}";

  // ทำการส่ง POST request
  HTTPClient http;
  http.begin("http://10.53.99.234:80/publish/");  // URL to the endpoint
  http.addHeader("Content-Type", "application/json");
  int httpResponseCode = http.POST(data);

  // แสดง response
  Serial.print("HTTP Response code: ");
  Serial.println(httpResponseCode);
  Serial.println(http.getString());

  http.end();

  // ไม่มีการทำงานใน loop
}