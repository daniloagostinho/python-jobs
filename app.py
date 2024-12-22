
from flask import Flask, request, jsonify
from flask_cors import CORS
import http.client
import json

app = Flask(__name__)
CORS(app)

@app.route('/search_jobs', methods=['GET'])
def search_jobs():
    query = request.args.get('query', 'react')
    location = request.args.get('location', 'Brazil')
    remote_only = 'true'  
    employment_types = request.args.get('employmentTypes', 'fulltime;parttime;intern;contractor')
    max_results = int(request.args.get('maxResults', '100'))  

    conn = http.client.HTTPSConnection("jobs-api14.p.rapidapi.com")
    headers = {
        'x-rapidapi-key': "KEY",
        'x-rapidapi-host': "jobs-api14.p.rapidapi.com"
    }

    all_jobs = []
    page = 1
    results_per_page = 20  

    try:
        while len(all_jobs) < max_results:
            url = (f"/v2/list?query={query}&location={location}&autoTranslateLocation=true"
                   f"&remoteOnly={remote_only}&employmentTypes={employment_types}&page={page}")

            conn.request("GET", url, headers=headers)
            res = conn.getresponse()
            data = res.read()

            response_data = json.loads(data.decode("utf-8"))
            jobs = response_data.get('jobs', [])

            if not jobs:
                break  

            all_jobs.extend(jobs)
            page += 1

        
        all_jobs = all_jobs[:max_results]
        return jsonify(jobs_data=json.dumps(all_jobs))

    except Exception as e:
        return jsonify(error=str(e)), 500

if __name__ == '__main__':
    app.run(debug=True)
