from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from necc import get_group_rankings, get_number_of_groups, get_national_placements, get_number_of_divisions

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
@cross_origin()
def hello_world():
    return "Ok."

@app.route("/nationals/<int:division>")
@cross_origin()
def nationals(division: int):
    ignoredQualified = request.args.get('ignoreQualified')
    ignoredQualified = "" if ignoredQualified == None else ignoredQualified
    if ignoredQualified.lower() == 'true':
        ignoredQualified = True
    else:
        ignoredQualified = False

    placements_list = get_national_placements(division, ignoredQualified)
    placements_list = jsonify(placements_list)
    return placements_list

@app.route("/seasonrankings/division/<int:division>/group/<int:group>")
@cross_origin()
def season_rankings(division: int, group: int):
    teams_list = get_group_rankings(division, group)
    teams_list = jsonify(teams_list)
    return teams_list

@app.route("/groupamount/<int:division>")
@cross_origin()
def group_amount(division: int):
    response = jsonify({"count" : get_number_of_groups(division)})
    return response

@app.route("/divisionamount")
@cross_origin()
def division_amount():
    response = jsonify({"count": get_number_of_divisions()})
    return response

if __name__ == "__main__":
    app.run(debug=True)