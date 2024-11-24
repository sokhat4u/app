from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

# Sample survey links for different hosts
host_links = {
    'insitesemea.decipherinc.com': 'https://notch.insights.supply/cb?token=47968ede-9aa3-4177-b870-5c845b3fe2a5&RID=',
    'go.makersights.com@spectrum': 'http://spectrumsurveys.com/surveydone?st=21&transaction_id=',
    'go.makersights.com': 'https://notch.insights.supply/cb?token=07197ab1-c4ee-4d1f-a67b-1d4013a56404&RID=',
    'pymnts.iad1.qualtrics.com': 'https://notch.insights.supply/cb?token=fcecb992-02e0-44d6-a803-f857c5a08b7e&RID=',
    'unitedminds.nu@cint': 'https://s.cint.com/Survey/Complete?ProjectToken=49c2f835-d221-4f1a-af26-6c4ede349f7e',
    'insights.surveynavigate.app': 'https://notch.insights.supply/cb?token=07acc3b2-400d-4219-8c33-67eb32577200f&RID=/',
    'survio': 'https://www.survio.com/survey/complete/',
    'm.survey.bz@toluna': 'http://ups.surveyrouter.com/trafficui/mscui/SOQualified.aspx?sname=xxxxx&TolunaEnc=4797&gid=xxxx',
    'research.potentia-insight.co.uk': 'https://notch.insights.supply/cb?token=ecb6b75f-4e65-4afc-a51e-bbf8743cca47&RID=',
    'survey.emi-rs.com': 'https://survey.emi-rs.com/end/complete/?scb=ZE7xxxx',
    'sur-tng.surveytng.com@samplecube': 'https://surveys.sample-cube.com/ending?RS=1&RID=xxxby666xxxxxxxxxxx&secret=9078',
    'brandresearch.qualtrics.com': 'https://notch.insights.supply/cb?token=0d0dc9e7-9541-4365-b4b2-b9522e4a21a7&RID=',
    'surveys.sago.com': 'https://notch.insights.supply/cb?token=312ef1b8-f520-4c8e-b19f-57d47ded4a9d&RID=',
    'us1se.voxco.com': 'https://notch.insights.supply/cb?token=d9af61cb-78d3-401d-93c1-d2ce388a8cd4&RID=',
    'singapore.decipherinc.com@spectrum': 'https://spectrumsurveys.com/surveydone?st=21&transaction_id=xxxxx&_k=2&_s=5b27d44e96894cf1c161e9636496d31c8debaffa',
    'sname': 'http://ups.surveyrouter.com/trafficui/mscui/SOQualified.aspx?sname=xxxx&TolunaEnc=4797&gid=xxxx',
    'no.surveymonkey.com': 'https://notch.insights.supply/cb?token=c7953959-d9a1-415b-a915-f15d2809d172&RID=',
    'survey.euro.confirmit.com@cint': 'https://s.cint.com/Survey/Complete?ProjectToken=fd0efe92-64c8-4fbc-a8c8-95d645101131',
    'redi.jtnpanel.com': 'https://notch.insights.supply/cb?token=716f0844-801e-48b4-b285-9f445577523f&RID=',
    'waler': 'https://notch.insights.supply/cb?token=288a1257-09e2-43e3-8765-e0c35d1affad&RID=',
    'surveys.irbureau.com': 'https://surveys.irbureau.com/panelistResponse?panelistResponse=103&rid=40979_ldhkhdplabipevoj_83',
    'research3.ipsosinteractive.com': 'https://dkr1.ssisurveys.com/projects/end?rst=1&psid=GlgtvJBILTIbJAXQvF-45Q',
    'surveysconnect.co.uk': 'https://notch.insights.supply/cb?token=68f41caf-9154-4775-991e-9f1e08ec325c&RID=',
    'web.appin.io@cint': 'https://s.cint.com/survey/return/62465b1f-4832-aab7-5c8b-6f6dd0d86995',
    'welcome.walr.com@spectrum': 'https://spectrumsurveys.com/surveydone?st=21&transaction_id=',
    'ema.focusvision.com@spectrum': 'https://spectrumsurveys.com/surveydone?st=21&transaction_id=xxxxx&ps_hash=2zh4imSX',
    'ema.focusvision.com': 'https://notch.insights.supply/cb?token=1499653c-5310-4cb2-9042-514f6b114713&RID=',
    'survey-d.yoursurveynow.com': 'https://notch.insights.supply/cb?token=ae73d5f2-56f0-4a2d-a235-328e8ac28275&RID=',
    'selfserve.decipherinc.com': 'https://notch.insights.supply/cb?token=7fe06e46-2d3b-4287-bbfd-dc57751406a0&RID=',
    'singapore.decipherinc.com': 'notch.insights.supply/cb?token=dc8ea18f-551a-471b-b9c4-01c0b54ed084&RID=',
    'nrc.decipherinc.com': 'https://notch.insights.supply/cb?token=ba250b92-688b-4556-ae5f-03b4c11eafce&RID=',
    'surveys.tapestryresearch.com': 'https://notch.insights.supply/cb?token=8aab3cbe-daf7-4462-a76d-0053285f1a10&RID=',
    'tes.decipherinc.com': 'https://notch.insights.supply/cb?token=5ad5cb3a-1213-42b8-8bfa-5dafaa68d008&RID=',
    'hub.decipherinc.com@cint': 'https://s.cint.com/Survey/Complete?ProjectToken=a82b3f38-baa0-4251-b64d-9288b7c4a952',
    '2cvresearch.decipherinc.com@cint': 'https://s.cint.com/Survey/Complete?ProjectToken=9825b707-ed93-4893-8070-0ab56e0d4bee',
    'Obsrvnow.com': 'https://notch.insights.supply/cb?token=f55dfca5-98b4-4916-a022-6f96909dce69&rid=',
    'surveyengine.pureprofile.com': 'https://surveyengine.pureprofile.com/api/v1/universal/payment/completed?num=1&ppid=rid-Z3XImv56QZKpnioQYI7VpQ',
    'surveys.harrisinsights.com': 'https://notch.insights.supply/cb?token=ba4eca57-554f-4cd6-8f58-64ee45661e60&RID=',
    'survey4.panelviewpoint.com': 'https://notch.insights.supply/cb?token=46f51506-06cb-4677-951e-607dd52630af&RID=',
    'surveys.lifepointspanel.com': 'https://notch.insights.supply/cb?token=880c4d83-d9ea-4406-a19b-ff23c3d5da36&RID=xxxxxxxxxxxx SSID from samplicio relevant id link xxxxxxxxx&cint_arid= xxxxxxxxxxxxx take ID from router.cint/clinet response link xxx dont put fingerprint id',
    'surveys.thepanelstation.com': 'https://notch.insights.supply/cb?token=6212d07b-2455-478a-b1a0-7e2b420b6887&RID=',
    'd8aspring.post-survey.com': 'https://notch.insights.supply/cb?token=92c87706-ecaf-4cc4-8456-9108b01a85e5&RID=',
    'surveys.ovationworldpanel.com': 'https://notch.insights.supply/cb?token=04651664-4715-4620-8f59-16a272ff3e4a&pid1=xxxxxxxxx&refid1=xxxxxxx&rid=xxxxxxxxx',
    'as-c1-web01.opinion.life': 'https://notch.insights.supply/cb?token=e770d4e9-3b78-4326-a3fa-f314983fb33d&RID=',
    'panel144.panelpulse.com': 'https://notch.insights.supply/cb?token=38de98e5-ebe9-4a7e-b81b-87ecb629cff9&RID='
    'survey.gavenze.com': 'https://notch.insights.supply/cb?token=6b8f8e7d-d27b-42f7-97f0-c1d5c51c6b67&RID=',
    'survey.researchautomators.se@cint': 'https://s.cint.com/Survey/Complete?ProjectToken=6aea9a90-7b3f-44bd-b0cb-ba0230b89538',
    'ups.surveyrouter.com@dkr': 'https://dkr1.ssisurveys.com/projects/end?rst=1&psid=P8dN_J4AWZigcx6mO4yQRg**&_k=1093&_s=38ef669880776bde376c6b370caf1d823ac0b1e867844d00b1dd56177a08d2cb',
    'api-icontrol.datadiggers-mr.com': 'https://api-icontrol.datadiggers-mr.com/processfinish?status=1&memberid=DD3F8oMKUaPtJWTFHmBnJ2x2',
    
    
    
    
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
    
