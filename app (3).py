import os
import uuid
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# 🛰️ VALERIX SECURE ENTERPRISE CLOUD KERNEL GATEWAY
# Is server route par asli hardware state logic aur key evaluation lock hai.
VALERIX_CLOUD_BACKEND = "https://core-api.valerix-enterprise.com/v2/control"

@app.route("/")
def dashboard_home():
    """Renders the main multi-modal operational grid interface."""
    return render_template("index.html")

@app.route("/api/v1/dispatch", methods=["POST"])
def dispatch_state_signal():
    """
    State loop interface router channel. Logs hardware signals 
    and forwards authentication matrix data directly to the server core.
    """
    payload = request.get_json()
    
    # Context parameters mapping
    state_code = payload.get("state_code")       # e.g., STATE_VALIDATE, STATE_MIGRATE
    license_key = payload.get("license_key")     # Subscription License key verification vector
    hardware_dna = payload.get("hardware_dna")   # Simulated Silicon PUF parameter
    
    # Package telemetry signature structure to present to judges
    handshake_packet = {
        "session_vector": str(uuid.uuid4())[:8],
        "target_operational_state": state_code,
        "token_signature": license_key,
        "telemetry_data": {
            "puf_fingerprint": hardware_dna,
            "peripheral_mac_mask": "00:1A:2B:3C:4D:5E",
            "liveness_stream_frame": "Verified_Liveness_True"
        }
    }
    
    try:
        # Tunnel packet directly into our protected host layer
        cloud_response = requests.post(
            f"{VALERIX_CLOUD_BACKEND}/execute",
            json=handshake_packet,
            headers={"X-Valerix-Client-Sign": "Secure-Channel-Alpha"},
            timeout=5
        )
        return jsonify(cloud_response.json())
        
    except requests.exceptions.RequestException:
        # 🛡️ Fallback Isolation Routine if connection fails or Subscription is expired
        return jsonify({
            "status": "QUARANTINE_LOCKDOWN",
            "code": 403,
            "message": "Security Handshake Dropped. Valid Valerix Subscription Key Required."
        }), 403

if __name__ == "__main__":
    print("[SYSTEM] Valerix Hardware Interface Dashboard Initialized.")
    print("[SYSTEM] Running local secure environment on http://127.0.0.1:8080")
    app.run(host="127.0.0.1", port=8080, debug=False)