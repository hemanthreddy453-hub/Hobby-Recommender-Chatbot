Python 3.13.2 (tags/v3.13.2:4f8bb39, Feb  4 2025, 15:23:48) [MSC v.1942 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> from flask import Flask, request, jsonify, render_template, redirect, url_for
... import requests
... #import os
... 
... app = Flask(__name__, template_folder='templates')
... app.secret_key = "your-secret-key-here"
... 
... GEMINI_API_KEY = "AIzaSyD4OuyUUsUWEc1V6B4T3LEuUuNS8t0jtHE"
... GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
... 
... @app.route("/")
... def home():
...     return render_template("index.html")
... 
... # Main application route (protected)
... @app.route("/main")
... def main():
...     return render_template("main.html")
... 
... # Login route
... @app.route("/login", methods=['GET', 'POST'])
... def login():
...     if request.method == 'POST':
...         # Basic authentication placeholder - replace with proper validation
...        return redirect(url_for('main'))
...     return render_template("login.html")
... 
... 
... @app.route("/signup", methods=['GET', 'POST'])
... def signup():
...     if request.method == 'POST':
...         # Process signup (add your registration logic here)
...         return redirect(url_for('main'))
...     return render_template("signup.html")
... 
... @app.route('/logo.png')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'logo.png', mimetype='image/vnd.microsoft.icon')

@app.route("/recommend", methods=["POST"])
def recommend():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    try:
        data = request.get_json()
        user_interest = data.get("interest")
        prompt = f"{user_interest}."
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        response = requests.post(GEMINI_API_URL, headers={"Content-Type": "application/json"}, json=payload)
        
        if response.status_code == 200:
            reply = response.json().get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No response")
            return jsonify({"recommendations": reply, "status": "success"})
        return jsonify({"error": f"Gemini API error: {response.status_code}"}), response.status_code
    except Exception as e:
        return jsonify({"error": "Server error", "details": str(e)}), 500

@app.route("/clear", methods=["POST"])
def clear_chat():
    return jsonify({"status": "success"})

if __name__ == "__main__":
