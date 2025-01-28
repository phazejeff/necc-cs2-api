from flask import Flask, request, jsonify
from necc import get_group_rankings, get_number_of_groups, get_national_placements

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Ok."

@app.route("/nationals")
def nationals():
    ignoredQualified = request.args.get('ignoreQualified')
    ignoredQualified = "" if ignoredQualified == None else ignoredQualified
    if ignoredQualified.lower() == 'true':
        ignoredQualified = True
    else:
        ignoredQualified = False

    placements_list = get_national_placements(ignoredQualified)
    placements_list = jsonify(placements_list)
    placements_list.headers.add("Access-Control-Allow-Origin", "*")
    return placements_list

@app.route("/seasonrankings/<int:group>")
def season_rankings(group: int):
    teams_list = get_group_rankings(group)
    teams_list = jsonify(teams_list)
    teams_list.headers.add("Access-Control-Allow-Origin", "*")
    return teams_list

@app.route("/groupamount")
def group_amount():
    response = jsonify({"count" : get_number_of_groups()})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == "__main__":
    app.run(debug=True)