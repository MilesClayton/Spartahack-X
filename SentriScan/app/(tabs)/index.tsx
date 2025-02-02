import React, { useEffect, useState } from "react";
import { View, Text, Image, ScrollView, StyleSheet, ActivityIndicator } from "react-native";
import io from "socket.io-client";
import axios from "axios";


// WebSocket & API URLs
const SOCKET_URL = "http://127.0.0.1:8081";
const API_URL = "http://127.0.0.1:8081/get-threats";

export default function Index() {
  const [detection, setDetection] = useState(null);
  const [loading, setLoading] = useState(true);
  const [pastDetections, setPastDetections] = useState([]);

  useEffect(() => {
    const socket = io(SOCKET_URL, { transports: ["websocket"] });

    socket.on("connect", () => {
      console.log("Connected to the server");
      setLoading(false);
    });

    socket.on("detection", (data) => {
      setDetection(data);
    });

    socket.on("disconnect", () => {
      console.log("Disconnected from the server");
    });

    return () => socket.disconnect();
  }, []);

  useEffect(() => {
    axios.get(API_URL)
      .then((response) => setPastDetections(response.data))
      .catch((error) => console.error("Error fetching past detections:", error));
  }, []);

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.header}>SentriScan - Real-Time Threat Detection</Text>

      {loading && <ActivityIndicator size="large" color="#0000ff" />}
      {!loading && detection ? (
        <View style={styles.resultContainer}>
          <Text style={styles.warning}>🚨 Firearm Detected!</Text>
          <Text>Confidence: {detection.confidence}%</Text>
          <Text>Object: {detection.object}</Text>
          <Text>📍 Location: {detection.location_data}</Text>
          <Text>🕒 {detection.timestamp}</Text>
          {detection.image_data && (
            <Image source={{ uri: `data:image/jpeg;base64,${detection.image_data}` }} style={styles.image} />
          )}
        </View>
      ) : (
        <Text style={styles.safe}>✅ No Threat Detected</Text>
      )}
    </ScrollView>
  );
}