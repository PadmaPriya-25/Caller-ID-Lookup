from flask import Flask, render_template, request
from twilio.rest import Client

app = Flask(__name__)

# Twilio credentials (replace with your own)
ACCOUNT_SID = ''
AUTH_TOKEN = ''

client = Client(ACCOUNT_SID, AUTH_TOKEN)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/lookup', methods=['POST'])
def lookup():
    phone_number = request.form['phone_number']
    try:
        lookup = client.lookups.v1.phone_numbers(phone_number).fetch(type="carrier")
        caller_info = {
            "phone_number": lookup.phone_number,
            "country_code": lookup.country_code,
            "carrier": lookup.carrier.get('name', 'N/A'),
            "line_type": lookup.carrier.get('type', 'N/A')
        }
    except Exception as e:
        caller_info = {"error": str(e)}

    return render_template('result.html', caller_info=caller_info)

if __name__ == '__main__':
    app.run(debug=True)

