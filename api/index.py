import requests
from datetime import datetime
import re
import json
from http.server import BaseHTTPRequestHandler

TELEGRAM_BOT_TOKEN = "8501492191:AAGzlwCiAnaXOeDxUjTTWE3oAW4RZ8824rU"
TELEGRAM_GROUP_ID = -1003761760398
IVAS_API_URL = "https://deedar.vercel.app/sms"

def fetch_sms():
    try:
        today_date = datetime.now().strftime("%d/%m/%Y")
        response = requests.get(IVAS_API_URL, params={"date": today_date, "limit": "10"}, timeout=30)
        data = response.json()
        
        if data.get("status") == "success":
            return data.get("otp_messages", [])
        return []
    except:
        return []

def send_to_telegram(phone, message):
    otp_match = re.search(r'\b(\d{4,8})\b', message)
    otp_text = otp_match.group(1) if otp_match else "N/A"
    
    text = f"""📱 New OTP Received!

📞 Number: {phone}
🔑 OTP: {otp_text}
💬 Message: {message[:200]}

────────────────
@mrchd112"""
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": TELEGRAM_GROUP_ID, "text": text}, timeout=10)
        print(f"Sent: {phone} | OTP: {otp_text}")
    except Exception as e:
        print(f"Error: {e}")

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        messages = fetch_sms()
        for msg in messages:
            send_to_telegram(msg.get("phone_number", ""), msg.get("otp_message", ""))
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "ok", "count": len(messages)}).encode())
    
    def do_POST(self):
        messages = fetch_sms()
        for msg in messages:
            send_to_telegram(msg.get("phone_number", ""), msg.get("otp_message", ""))
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "ok", "count": len(messages)}).encode())
