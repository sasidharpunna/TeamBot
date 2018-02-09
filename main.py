from flask import Flask
from flask import request
from flask import make_response
import argparse
import pandas as pd
import json

parser = argparse.ArgumentParser()
parser.add_argument("f_path", help="File_Path Or File_Name")
args = parser.parse_args()
File_Path = args.f_path
df = pd.read_excel(File_Path)
ddf = df[df['Technology'] == 'BIDW']['Customer ID']
hd = df.head()
sdf = hd.to_html()

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


@app.route('/', methods=['GET'])
def test():
    return sdf


@app.route('/<string:name>', methods=['GET'])
def test0(name):
    tech = df[[name, 'Project Name', 'Project ID']]
    tt = tech.to_html()
    return tt


@app.route('/<string:name>/<string:name1>', methods=['GET'])
def test10(name, name1):
    tech = df.loc[df[name] == name1, [name, 'Project ID', 'Project Name']]
    tt = tech.to_html()
    return tt


if __name__ == '__main__':
  app.run()
