import os
import sys
import json
import pymongo
from bottle import route, run, template
from pprint import pprint

print("Running using: %s" % sys.executable)

html_template = r'''
<title>Python Env</title>
<body>
<h1>Python Env</h1>
<ul>
  % for name, value in envlist.items():
    <li><b>{{name}}</b>: <tt>{{value}}</tt></li>
  % end
</ul>
Extra stuff: <pre>{{extra}}</pre>
</body>
'''

@route('/')
def index():
    result = None
    try:
      services = json.loads(os.environ['VCAP_SERVICES'])
      mongo_uri = services["mongodb"][0]["credentials"]["uri"]
      client = pymongo.MongoClient(mongo_uri)
      db = client.mydb
      business = {'name': 'SUSE', 'hq': 'Nürnberg'}
      result = db.reviews.insert_one(business)
    except:
      result = sys.exc_info()
    if isinstance(result, pymongo.results.InsertOneResult):
      result = (result.inserted_id, result.acknowledged)
    return template(html_template, envlist=os.environ, extra=result)

run(host='0.0.0.0', port=int(os.getenv("PORT", 8080)))
