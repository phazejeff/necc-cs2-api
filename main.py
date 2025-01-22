from flask import Flask, request
from database.models import Placement
from playhouse.shortcuts import model_to_dict
from necc import get_group_rankings

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Ok."

@app.route("/nationals")
def nationals():
    placements = Placement.select().order_by(Placement.national_points.desc())
    ignoredQualified = request.args.get('ignoreQualified')
    ignoredQualified = "" if ignoredQualified == None else ignoredQualified
    if ignoredQualified.lower() == 'true':
        placements = placements.where(Placement.fall_playoff_placement != 1)
    placements_list: list[dict] = []
    for placement in placements:
        placements_list.append(model_to_dict(placement))
    
    return placements_list

@app.route("/seasonrankings/<int:group>")
def season_rankings(group: int):
    teams_list = get_group_rankings(group)
    
    return teams_list

if __name__ == "__main__":
    app.run(debug=True)