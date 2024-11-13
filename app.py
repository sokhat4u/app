from flask import Flask, render_template, request, jsonify
import random
import string

app = Flask(__name__)

# Sample survey links for different hosts
host_links = {
    'insitesemea.decipherinc.com': 'https://notch.insights.supply/cb?token=47968ede-9aa3-4177-b870-5c845b3fe2a5&RID=/',
    'go.makersights.com@spectrum': 'http://spectrumsurveys.com/surveydone?st=21&transaction_id=/',
    'go.makersights.com': 'https://notch.insights.supply/cb?token=07197ab1-c4ee-4d1f-a67b-1d4013a56404&RID=/',
    'pymnts.iad1.qualtrics.com': 'https://notch.insights.supply/cb?token=fcecb992-02e0-44d6-a803-f857c5a08b7e&RID=/',
    'unitedminds.nu@cint': 'https://s.cint.com/Survey/Complete?ProjectToken=49c2f835-d221-4f1a-af26-6c4ede349f7e',
    'insights.surveynavigate.app': 'https://notch.insights.supply/cb?token=07acc3b2-400d-4219-8c33-67eb32577200f&RID=/',
    'survio': 'https://www.survio.com/survey/complete/',
    'm.survey.bz@toluna': 'http://ups.surveyrouter.com/trafficui/mscui/SOQualified.aspx?sname=xxxxx&TolunaEnc=4797&gid=xxxx',
    'research.potentia-insight.co.uk': 'https://notch.insights.supply/cb?token=ecb6b75f-4e65-4afc-a51e-bbf8743cca47&RID=',
    'survey.emi-rs.com': 'https://survey.emi-rs.com/end/complete/?scb=ZE7xxxx',
    'sur-tng.surveytng.com@samplecube': 'https://surveys.sample-cube.com/ending?RS=1&RID=xxxby666xxxxxxxxxxx&secret=9078',
    'brandresearch.qualtrics.com': 'https://notch.insights.supply/cb?token=0d0dc9e7-9541-4365-b4b2-b9522e4a21a7&RID=',
    'surveys.sago.com': 'https://notch.insights.supply/cb?token=312ef1b8-f520-4c8e-b19f-57d47ded4a9d&RID=',
}

# Function to save unknown host names
def save_unknown_host(host_name):
    with open("unknown_hosts.txt", "a") as file:
        file.write(host_name + "\n")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_link():
    data = request.get_json()
    host_name = data.get('hostName').lower()

    # Remove 'https://' or 'http://' prefix from the host_name
    normalized_host_name = re.sub(r'^https?://', '', host_name)

    if normalized_host_name in host_links:
        link = host_links[normalized_host_name]
        return jsonify({'success': True, 'link': link})
    else:
        # Save unknown host name
        save_unknown_host(normalized_host_name)
        return jsonify({
            'success': False,
            'error': 'Host not found'
        })

if __name__ == '__main__':
    app.run(debug=True)
