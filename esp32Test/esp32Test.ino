#include <WiFi.h>
#include <WiFiClient.h>
#include <WiFiAP.h>
#include <WebServer.h>

const char* ssid = "CS112";
const char* password = "cs@123456";
const int port = 80;
String receivedData;

WebServer server(port);

void setup() {
  Serial.begin(115200);
  delay(100);

  // Connect to WiFi
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi..");
  }
  Serial.println("Connected to WiFi");

  // Print the IP address
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  server.on("/data", HTTP_POST, [](){
    receivedData = server.arg("plain");
    //Serial.print("Received Data: ");
    Serial.println(receivedData);

    // Transmit received data to Arduino through serial communication
    Serial1.println(receivedData); 

    server.send(200, "text/plain", "Data received successfully");
  });

  server.begin();
  Serial.println("HTTP server started");
}

void loop() {
  server.handleClient();
}
