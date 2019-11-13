from jupyterhub.auth import Authenticator
from tornado import gen
import pyjwt
import requests
import configparser
import grp
import subprocess

class ClueJupyterAuthenticator(Authenticator):

    def authenticate(self, handler, data):
        cp = configparser.RawConfigParser()
        cp.read('jupyter.cfg')
        api_key = cp.get("authentication", "clue_api_key")
        headers= {"user_key": api_key}

        base_url = cp.get("authentication", "clueAuthenticationEndPoint")
        return_to = ""
        url = base_url + "?returnTo=" + return_to

        username = data['username']
        password = data['password']
        payload = {"username": username, "password": password}

        r = requests.post(url, data=payload, headers=headers)

        secret = cp.get("authentication", "jwtSecretToken")
        decoded = pyjwt.decode(r.text, secret)

        self.user = decoded[0] || decoded
        self.roles = [r.role_id for r in self.user.role]


    def authorize(self):
        self._validate_roles()
        self._authorize()

    def _validate_roles(self):
        for role in self.roles:
            try:
                grp.getgrnam(role)
            except KeyError:
                exit_value = subprocess.call(["groupadd", role])
                if exit_value != 0:
                    raise Exception("Failed to create new group {} with exit value {} ".format(role, exit_value))
                else:
                    continue

    def _authorize(self):
        # usermod -G "comma-separated group string" will remove user from any groups which are not within the group string
        string_roles = ",".join(self.roles)
        exit_value = subprocess.call("usermod", "-G", string_roles, self.user)
        if exit_value != 0:
            raise Exception("Failed to update groups {} for user {}".format(string_roles, self.user))

