from flask import Blueprint

from CTFd.models import Challenges, db
from CTFd.plugins import register_plugin_assets_directory
from CTFd.plugins.challenges import CHALLENGE_CLASSES, BaseChallenge
from CTFd.plugins.migrations import upgrade

from pathlib import Path

import urllib.parse
import requests
import yaml
import os

conf = None
plugin_name = __name__.split('.')[-1]

class CustomDashboardChallenge(Challenges):
    __mapper_args__ = {"polymorphic_identity": "custom"}
    id = db.Column(
        db.Integer, db.ForeignKey("challenges.id", ondelete="CASCADE"), primary_key=True
    )

    def __init__(self, *args, **kwargs):
        super(CustomDashboardChallenge, self).__init__(**kwargs)


class CustomDashboardChallengeControler(BaseChallenge):
    id = "custom"  # Unique identifier used to register challenges
    name = "custom"  # Name of a challenge type
    templates = {  # Templates used for each aspect of challenge editing & viewing
        "create": f"/plugins/{plugin_name}/assets/create.html",
        "update": f"/plugins/{plugin_name}/assets/update.html",
        "view": f"/plugins/{plugin_name}/assets/view.html",
    }
    scripts = {  # Scripts that are loaded when a template is loaded
        "create": f"/plugins/{plugin_name}/assets/create.js",
        "update": f"/plugins/{plugin_name}/assets/update.js",
        "view": f"/plugins/{plugin_name}/assets/view.js",
    }
    # Route at which files are accessible. This must be registered using register_plugin_assets_directory()
    route = f"/plugins/{plugin_name}/assets/"
    # Blueprint used to access the static_folder directory.
    blueprint = Blueprint(
        plugin_name, __name__, template_folder="templates", static_folder="assets"
    )
    challenge_model = CustomDashboardChallenge

    @classmethod
    def solve(cls, user, team, challenge, request):
        super().solve(user, team, challenge, request)
        requests.post(urllib.parse.urljoin(conf['url'], 'solve'), headers={"Authorization": f"Token {conf['token']}"}, json={"chall": challenge.id, "team": team.id})

def loadconfig():
    global conf
    dir_path = Path(__file__).parent.resolve()
    with open(os.path.join(dir_path, 'config.yml')) as f:
        conf = yaml.load(f, Loader=yaml.FullLoader)

def load(app):
    loadconfig()
    upgrade(plugin_name=plugin_name)
    CHALLENGE_CLASSES["custom"] = CustomDashboardChallengeControler
    register_plugin_assets_directory(
        app, base_path=f"/plugins/{plugin_name}/assets/"
    )
