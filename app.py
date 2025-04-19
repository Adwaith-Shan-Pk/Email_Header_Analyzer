from flask import Flask, render_template, request
import email
from email import policy
from io import StringIO

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    analysis = None
    error = None
    if request.method == 'POST':
        header_data = request.form.get('header_data')
        if header_data:
            try:
                # Prepend a dummy line because email parser expects the first line to be 'From '
                # However, for headers only, this might not be necessary, but good practice for full emails.
                # Let's try parsing directly first.
                # If it fails, we might need to adjust.
                msg = email.message_from_string(header_data, policy=policy.default)
                
                analysis = {}
                for key, value in msg.items():
                    analysis[key] = value
                    
                # Example: Extract specific common headers
                analysis['Subject'] = msg.get('Subject', 'N/A')
                analysis['From'] = msg.get('From', 'N/A')
                analysis['To'] = msg.get('To', 'N/A')
                analysis['Date'] = msg.get('Date', 'N/A')
                analysis['Received'] = msg.get_all('Received', []) # Get all Received headers

            except Exception as e:
                error = f"Error parsing headers: {e}"
        else:
            error = "Please paste the email header data."
            
    return render_template('index.html', analysis=analysis, error=error)

if __name__ == '__main__':
    app.run(debug=True)