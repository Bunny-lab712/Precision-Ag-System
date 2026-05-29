import gradio as gr
import pandas as pd
import datetime
import time
import random

# --- 1. STATE & MOCK DATA ---
# Real-time sensor state with base values for historical generation
zone_data = {
    "Zone 1 (North Field)": {"status": "✅ Healthy", "moisture": "45%", "ph": "6.5", "m_base": 45},
    "Zone 2 (East Field)": {"status": "⚠️ Low Moisture", "moisture": "28%", "ph": "6.4", "m_base": 30},
    "Zone 3 (South Field)": {"status": "💧 High Moisture", "moisture": "65%", "ph": "5.8", "m_base": 60},
    "Zone 4 (West Field)": {"status": "✅ Optimal", "moisture": "50%", "ph": "6.8", "m_base": 50}
}

disease_classes = ["Tomato_Early_blight", "Apple_scab", "Corn_Common_rust", "Healthy_Leaf", "Potato_Late_blight"]
logs = ["[System] Booting Command Center..."]
logs.insert(0, "[System] Establishing MQTT broker connection for ESP32 nodes...")
logs.insert(0, "[System] All nodes online. Drone is on Standby.")

# --- 2. BACKEND LOGIC FUNCTIONS ---
def generate_history_plot(zone):
    """Generates a 30-day mock history for the selected zone using pandas."""
    dates = pd.date_range(end=datetime.date.today(), periods=30)
    base = zone_data[zone]["m_base"]
    # Create realistic-looking fluctuating data
    moisture_levels = [max(10, min(100, base + random.randint(-8, 8))) for _ in range(30)]
    df = pd.DataFrame({"Date": dates, "Moisture (%)": moisture_levels})
    return df

def update_zone_display(zone_choice):
    """Updates the dashboard when a new zone is clicked."""
    data = zone_data[zone_choice]
    history_df = generate_history_plot(zone_choice)
    return data["status"], data["moisture"], data["ph"], history_df

def trigger_esp_alert():
    """Simulates an ESP-NOW alert WITH Weather API Logic."""
    time_now = datetime.datetime.now().strftime('%H:%M:%S')
    target = random.choice(["Zone 2 (East Field)", "Zone 3 (South Field)"])

    # 1. Weather Check Logic
    weather_conditions = ["Clear", "Clear", "Clear", "Raining"]
    current_weather = random.choice(weather_conditions)

    logs.insert(0, f"[{time_now}] 🚨 ESP-NOW ALERT: Sensor threshold breached in {target}.")

    if current_weather == "Raining":
        logs.insert(0, f"[{time_now}] ⛈️ WEATHER OVERRIDE: Rain detected. Drone dispatch cancelled to protect hardware.")
        return "🚁 GROUNDED (Weather Hold)", "\n".join(logs[:8])

    # 2. Dispatch Logic
    logs.insert(0, f"[{time_now}] ☀️ Weather Clear. Drone Dispatched to {target}!")
    return "🚁 IN FLIGHT (Dispatched)", "\n".join(logs[:8])

def simulate_ai_scan(img):
    """Simulates Drone Image Capture, MobileNetV2 Inference, and SMS alerting."""
    time_now = datetime.datetime.now().strftime('%H:%M:%S')

    if img is None:
        logs.insert(0, f"[{time_now}] ⚠️ Error: Camera feed empty.")
        return "🚁 STANDBY", "\n".join(logs[:8]), None, "No Action"

    logs.insert(0, f"[{time_now}] 📸 Image captured. Running Edge AI (MobileNetV2)...")

    primary_disease = random.choice(disease_classes)
    confidence = random.uniform(0.85, 0.98)

    results = {
        primary_disease: confidence,
        "Secondary Risk": 1.0 - confidence - 0.01,
        "Healthy_Background": 0.01
    }

    logs.insert(0, f"[{time_now}] ✅ AI Diagnosis: {primary_disease} ({confidence*100:.1f}%).")

    # Automated SMS Logic
    sms_status = "Standby"
    if primary_disease != "Healthy_Leaf" and confidence > 0.90:
        logs.insert(0, f"[{time_now}] 📱 AUTOMATION: Severe disease detected. SMS Alert dispatched to Farmer.")
        sms_status = f"✅ Sent: '{primary_disease} detected in field. Action required.'"
    else:
        sms_status = "No alert needed (Healthy or Low Confidence)"

    return "🚁 RETURNING TO BASE", "\n".join(logs[:8]), results, sms_status


# --- 3. BUILD THE FRONTEND INTERFACE ---
with gr.Blocks(theme=gr.themes.Default()) as app:
    gr.Markdown("# 🚁 Advanced Farm Command Center")
    gr.Markdown("Integrating **ESP-NOW Sensors**, **MobileNetV2 Vision**, **Weather APIs**, and **Automated SMS**.")

    # TOP ROW: Live Metrics
    with gr.Row():
        gr.Number(value=94.2, label="AI Accuracy (%)", interactive=False)
        gr.Number(value=55, label="Battery Savings (%)", interactive=False)
        gr.Textbox(value="Connected via MQTT", label="ESP32 Network Status", interactive=False)
        drone_status = gr.Textbox(value="🚁 STANDBY", label="Live Drone Status", interactive=False)

    # MIDDLE ROW: Map, Sensors, and Analytics
    with gr.Row():
        # Left: Map & Selection
        with gr.Column(scale=1):
            gr.Markdown("### 📍 Field Map (Karimnagar Region)")
            # Embedding a live OpenStreetMap iframe centered roughly on your region
            gr.HTML("""
                <iframe width="100%" height="200" frameborder="0" scrolling="no" marginheight="0" marginwidth="0"
                src="https://www.openstreetmap.org/export/embed.html?bbox=79.10,18.40,79.15,18.45&layer=mapnik"
                style="border: 1px solid black; border-radius: 8px;"></iframe>
            """)
            zone_selector = gr.Radio(choices=list(zone_data.keys()), value="Zone 1 (North Field)", label="Select Zone to Inspect")

            with gr.Row():
                z_status = gr.Textbox(label="Health Status")
                z_moisture = gr.Textbox(label="Current Moisture")
                z_ph = gr.Textbox(label="Current pH")

            alert_btn = gr.Button("⚠️ Trigger ESP32 Hardware Alert", variant="stop")

        # Right: Historical Data
        with gr.Column(scale=1):
            gr.Markdown("### 📈 30-Day Soil Moisture Analytics")
            history_plot = gr.LinePlot(x="Date", y="Moisture (%)", title="Moisture Trend", height=280)

    gr.Markdown("---")

    # BOTTOM ROW: AI Vision and Logs
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 🧠 Drone AI Vision Console (MobileNetV2)")
            img_input = gr.Image(type="pil", label="Drone Camera / Upload Leaf Image", height=200)
            scan_btn = gr.Button("🔍 Execute Drone Scan & Analyze", variant="primary")
            ai_output = gr.Label(num_top_classes=3, label="AI Diagnosis & Confidence")
            sms_out = gr.Textbox(label="Automated SMS Gateway System", interactive=False)

        with gr.Column(scale=1):
            gr.Markdown("### 📝 Master System Event Tracker")
            log_out = gr.Textbox(label="Live Console", lines=15, value="\n".join(logs), interactive=False)

    # --- 4. WIRE UP THE INTERACTIVITY ---
    zone_selector.change(fn=update_zone_display, inputs=zone_selector, outputs=[z_status, z_moisture, z_ph, history_plot])
    app.load(fn=update_zone_display, inputs=zone_selector, outputs=[z_status, z_moisture, z_ph, history_plot])

    alert_btn.click(fn=trigger_esp_alert, inputs=None, outputs=[drone_status, log_out])
    scan_btn.click(fn=simulate_ai_scan, inputs=img_input, outputs=[drone_status, log_out, ai_output, sms_out])

# --- 5. LAUNCH ---
if __name__ == "__main__":
    app.launch(share=True)
