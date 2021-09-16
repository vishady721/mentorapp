from flask import Blueprint, Response, request, jsonify, make_response, render_template, redirect, url_for
from config import config_settings
import requests
import config

email_bp = Blueprint("email", __name__, url_prefix='/email')

@email_bp.route('/send_emails', methods=['GET'])
def test():
    from app.models import Matches
    from app import app
    def send_email(mentor_email, team_email, team_id, mentor_id):
        app.config.from_object(config_settings['production'])
        return requests.post(
            "https://api.mailgun.net/v3/my.hackmit.org/messages",
            auth=("api", app.config['MAILGUN_API']),
            data={"from": "Test User <mentor@my.hackmit.org>",
                "to": [mentor_email, team_email],
                "subject": "test matches",
                "text": "goomonin ur team is {0} and mentor is {1}".format(team_id, mentor_id)})

    all_matches = Matches.serialize()
    for row in all_matches:
        print(send_email(all_matches[row][2], all_matches[row][0], row, all_matches[row][1]))
    return "emails sent", 200
