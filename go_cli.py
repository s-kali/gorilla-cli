# Copyright 2023 https://github.com/ShishirPatil/gorilla
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
import os
import sys
import uuid
import fcntl
import platform
import requests
import subprocess
import argparse
import termios
import urllib.parse
import sys
from halo import Halo
import go_questionary

__version__ = "0.0.11"  # current version
SERVER_URL = "https://cli.gorilla-llm.com"
USERID_FILE = os.path.expanduser("~/.gorilla-cli-userid")
GORILLA_EMOJI = "🦍 " if go_questionary.try_encode_gorilla() else ""
WELCOME_TEXT = f"""===***===
{GORILLA_EMOJI}Welcome to Gorilla-CLI! Enhance your Command Line with the power of LLMs! 

Simply use `gorilla <your desired operation>` and Gorilla will do the rest. For instance:
    gorilla generate 100 random characters into a file called test.txt
    gorilla get the image ids of all pods running in all namespaces in kubernetes
    gorilla list all my GCP instances

A research prototype from UC Berkeley, Gorilla-CLI ensures user control and privacy:
 - Commands are executed only with explicit user approval.
 - While queries and error (stderr) logs are used to refine our model, we NEVER gather output (stdout) data.

Visit github.com/gorilla-llm/gorilla-cli for examples and to learn more!
===***==="""


def main():
    args = sys.argv[1:]
    user_input = " ".join(args)

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Gorilla CLI Help Doc")
    parser.add_argument("command_args", nargs='*', help="Prompt to be inputted to Gorilla")

    with Halo(text=f"{GORILLA_EMOJI}Loading", spinner="dots"):
        try:
            data_json = {
                "user_id": "1000",
                "user_input": user_input,
                "interaction_id": str(uuid.uuid4()),
                "system_info": "Linux"
            }
            response = requests.post(
                f"{SERVER_URL}/commands_v2", json=data_json, timeout=30
            )
            commands = response.json()
        except requests.exceptions.RequestException as ignored:
            print("Server is unreachable.")
            print("Try updating Gorilla-CLI with 'pip install --upgrade gorilla-cli'")
            return

    if commands:
        for cmd in commands[:-1]:
            print(cmd)


if __name__ == "__main__":
    main()
