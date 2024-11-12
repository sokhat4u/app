from flask import Flask, render_template, request, jsonify
import random
import string

app = Flask(__name__)

# Sample survey links for different hosts
host_links = {
    'https://survey.euro.confirmit.com': 'https://notch.insights.supply/cb?token=ecb6b75f-4e65-4afc-a51e-bbf8743cca47&RID=672852d4-c7c8-e42b-d995-db04b19f6a2e/',
    'https://surveyengine.pureprofile.com': 'https://surveyengine.pureprofile.com/api/v1/universal/payment/completed?num=1&ppid=rid-BAk1730643016KqA/',
    'typeform': 'https://form.typeform.com/to/complete/',
    'https://emea.focusvision.com@cint': 'https://s.cint.com/Survey/Complete',
    'zoho': 'https://survey.zoho.com/complete/',
    'survio': 'https://www.survio.com/survey/complete/'
}

def generate_random_string():
    # Generate a random string to append to the URL
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_link():
    data = request.get_json()
    host_name = data.get('hostName').lower()

    if host_name in host_links:
        link = host_links[host_name] + generate_random_string()
        return jsonify({'success': True, 'link': link})
    else:
        return jsonify({
            'success': False,
            'error': 'Host not found'
        })

if __name__ == '__main__':
    app.run(debug=True)
