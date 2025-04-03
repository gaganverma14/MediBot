# gemini api- AIzaSyAPmTdTKNkm-fBoV1MXzb_Qd9SpblSCYo8
# ngrok api - 2uamTR2ecicmjJf83LJeFpluLEO_86rcFVJ4UFGC1H2mjtsnk

import time
import torch
from flask import Flask, request, jsonify
from flask_cors import CORS
from pyngrok import ngrok
import google.generativeai as genai


API_KEY = "AIzaSyAPmTdTKNkm-fBoV1MXzb_Qd9SpblSCYo8"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

NGROK_AUTH_TOKEN = "2uamTR2ecicmjJf83LJeFpluLEO_86rcFVJ4UFGC1H2mjtsnk"
ngrok.set_auth_token(NGROK_AUTH_TOKEN)

def restart_ngrok():
    while True:
        try:
            public_url = ngrok.connect(5000).public_url
            print(f"Ngrok Public URL: {public_url}")
            return public_url
        except Exception as e:
            print(f"Ngrok failed: {e}. Retrying in 10 seconds...")
            time.sleep(10)

public_url = restart_ngrok()


SYSTEM_PROMPT = (
    "You are Dr. MediBot, a highly trained AI medical expert with qualifications equivalent to an MBBS, MD (Internal Medicine), "
    "and DM (Super-Specialist in Cardiology, Neurology, and Endocrinology). You provide medical advice following evidence-based clinical guidelines "
    "from Harrison's Principles of Internal Medicine, Nelson's Pediatrics, WHO, CDC, FDA, and NHS.\n\n"
    
    "You are specifically trained to be a medical chatbot for common people, offering guidance in a simple, understandable, and professional manner.\n"
    
    "If someone asks 'Who are you?' or 'Who trained you?', always respond with: 'I am Dr. MediBot, an AI medical assistant trained to provide evidence-based health information to the public.'\n\n"
    
    "If the user greets you (e.g., 'hi', 'hello', 'hey'), respond in a friendly manner such as: 'Hello! How can I assist you today?'\n"
    
    "Guidelines for Your Response:\n"
    "1. Be empathetic and non-judgmental.\n"
    "2. Detailed Medical Explanation - Provide expert-level knowledge on diseases, symptoms, diagnostics, and treatments.\n"
    "3. Evidence-Based Treatment Plans - Base responses on clinical trial data, medical textbooks, and guidelines.\n"
    "4. Strictly Professional Tone - Maintain a formal, doctor-like manner (avoid casual chat).\n"
    "5. Differential Diagnosis - Consider multiple conditions based on symptoms and risk factors.\n"
    "6. Emergency Considerations - Indicate when urgent medical care is required.\n\n"
)


app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return "MediChat AI is Running! Use the /chat endpoint."

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "").strip().lower()

    if not user_message:
        return jsonify({"reply": "⚠️ Please enter a valid medical question."})

    
    greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]
    if user_message in greetings:
        return jsonify({"reply": "Hello! How can I assist you today?"})

    full_prompt = f"{SYSTEM_PROMPT}\nPatient's Question: {user_message}\n\nDoctor's Response:"

    response = model.generate_content(full_prompt)

   
    reply_text = getattr(response, "text", "⚠️ Sorry, I couldn't generate a response.")

    return jsonify({"reply": reply_text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)
