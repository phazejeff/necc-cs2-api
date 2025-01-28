from flask import Flask, request, jsonify
from database.models import Placement, Team
from playhouse.shortcuts import model_to_dict
from necc import get_group_rankings, get_number_of_groups

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Ok."

@app.route("/nationals")
def nationals():
    placements: list[Placement] = (Placement
        .select(Placement, Team)
        .join(Team, on=(Placement.team_id == Team.team_id), attr='team')
        .order_by(Placement.national_points.desc())
        )
    print(placements[0].team)
    ignoredQualified = request.args.get('ignoreQualified')
    ignoredQualified = "" if ignoredQualified == None else ignoredQualified
    if ignoredQualified.lower() == 'true':
        placements = placements.where(Placement.fall_playoff_placement != 1)
    placements_list: list[dict] = []
    for placement in placements:
        placement_dict = model_to_dict(placement)
        placement_dict['team'] = model_to_dict(placement.team)
        placements_list.append(placement_dict)
    
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