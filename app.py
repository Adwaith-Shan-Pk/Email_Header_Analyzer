from flask import Flask, render_template, request
import email
from email import policy
from io import StringIO
import re 
import requests
import os 

app = Flask(__name__)

# Regex to find IPv4 and IPv6 addresses
IP_REGEX = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b|\b(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}\b|\b(?:[a-fA-F0-9]{1,4}:){1,7}:(?:[a-fA-F0-9]{1,4}:){1,7}\b')

# --- IP Reputation Check  ---.
ABUSEIPDB_API_KEY = os.getenv('ABUSEIPDB_API_KEY')
ABUSEIPDB_ENDPOINT = 'https://api.abuseipdb.com/api/v2/check'

def check_ip_reputation(ip_address):
    """Checks the reputation of an IP address using the AbuseIPDB API."""
    if not ABUSEIPDB_API_KEY or ABUSEIPDB_API_KEY == 'YOUR_ABUSEIPDB_API_KEY':
        return "API Key Missing"

    headers = {
        'Accept': 'application/json',
        'Key': ABUSEIPDB_API_KEY
    }
    params = {
        'ipAddress': ip_address,
        'maxAgeInDays': '90' # Check reports within the last 90 days
    }
    try:
        response = requests.get(ABUSEIPDB_ENDPOINT, headers=headers, params=params, timeout=10)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        data = response.json().get('data', {})

        if data.get('isWhitelisted'):
            return "Whitelisted"
        abuse_score = data.get('abuseConfidenceScore', 0)
        if abuse_score >= 75:
            return f"Malicious (Score: {abuse_score})"
        elif abuse_score >= 25:
            return f"Suspicious (Score: {abuse_score})"
        else:
            return f"Clean (Score: {abuse_score})"

    except requests.exceptions.RequestException as e:
        print(f"Error checking IP {ip_address}: {e}") # Log error to console
        return f"Error Checking ({type(e).__name__})"
    except Exception as e:
        print(f"Unexpected error checking IP {ip_address}: {e}")
        return "Error Checking (Unexpected)"


@app.route('/', methods=['GET', 'POST'])
def index():
    analysis = None
    error = None
    if request.method == 'POST':
        header_data = request.form.get('header_data')
        if header_data:
            try:
                
                
                
            
                msg = email.message_from_string(header_data, policy=policy.default)

                analysis = {}
                for key, value in msg.items():
                 
                    existing = analysis.get(key)
                    if existing:
                        if isinstance(existing, list):
                            analysis[key].append(value)
                        else:
                            analysis[key] = [existing, value]
                    else:
                        analysis[key] = value

               
                received_headers = msg.get_all('Received', [])
                analysis['Received'] = received_headers

              
                extracted_ips = set() 
                for header in received_headers:
                    found_ips = IP_REGEX.findall(header)
                    for ip in found_ips:
                       
                       
                
                        if not (ip.startswith('192.168.') or ip.startswith('10.') or 
                                (ip.startswith('172.') and 16 <= int(ip.split('.')[1]) <= 31) or 
                                ip == '127.0.0.1' or ip == '::1'):
                            extracted_ips.add(ip)
                
                if extracted_ips:
                    ip_reputation_results = {}
                    sorted_ips = sorted(list(extracted_ips))
                    for ip in sorted_ips:
                        reputation = check_ip_reputation(ip)
                        ip_reputation_results[ip] = reputation
                    analysis['IP Reputation'] = ip_reputation_results 

            except Exception as e:
                error = f"Error parsing headers: {e}"
        else:
            error = "Please paste the email header data."

    return render_template('index.html', analysis=analysis, error=error)

if __name__ == '__main__':
    app.run(debug=True)