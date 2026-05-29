# AI-Powered Precision Agriculture Drone System 🚁🌾

**Developed by:** AdhyaA Labs

## Overview
This project integrates edge AI, IoT ground sensors, and drone technology to create an automated, event-driven precision agriculture system. By utilizing an ESP32-based sensor network and a lightweight MobileNetV2 model, this system identifies distressed crop zones, dispatches an autonomous drone for visual inspection, and provides real-time disease diagnostics to farmers.

## Core Architecture
* **The Ground Sensor Node (ESP32):** Monitors soil moisture and pH. Triggers alerts via the ESP-NOW protocol when thresholds are breached.
* **The Drone/Edge Layer:** Processes incoming sensor data and utilizes a highly optimized TensorFlow Lite model to analyze crop imagery.
* **The Command Center (Gradio):** A Full-Stack web dashboard providing live satellite mapping, 30-day historical analytics, weather-aware flight logic, and automated SMS alerts for severe crop diseases.

## Repository Contents
* `Drone.ipynb`: The primary Jupyter Notebook containing the data pipeline, MobileNetV2 training script, and the Gradio web dashboard interface.
* `crop_health_model.h5`: The trained deep learning model achieving ~94.2% diagnostic accuracy.
* `USREM58929.pdf` & `project (1).pdf`: Official project documentation, research methodologies, and system architecture blueprints.
* `AI-Powered Precision Agriculture Drone ...`: Presentation deck detailing the hardware-software integration.

## Technologies Used
* **Machine Learning:** TensorFlow, Keras, MobileNetV2
* **IoT & Hardware:** C++, Arduino IDE, ESP32-S3, ESP-NOW Protocol
* **Interface & Backend:** Python, Gradio, Pandas, MQTT

## Future Enhancements
* Hardware integration with real-time MQTT brokers.
* Deployment of the `.tflite` model directly onto the ESP32-S3 drone camera module.