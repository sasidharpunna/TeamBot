from flask import Flask
from flask import request
from flask import make_response
import pandas as pd
import json

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def makeWebhookResult(req):
    if req.get("result").get("action") != "ProjectStatus":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    status = parameters.get("Status")
    df = pd.read_excel('Sample_Project_Stats.xls')
    hd = df.head()
    name = 'RISK'
    output = df.loc[df[name] == status, ['Project Name']].to_string(header=None, index=False)
    newoutput = output.replace("          ", "").replace("\n", " & ")
    print(newoutput)

    speech = "The list of projects with Status " + status + " are " + newoutput
    print("Response:")
    print(speech)
    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        #"contextOut": [],
        "source": "TeaMBot"
    }

if __name__ == '__main__':
  app.run()
