import sys
from pathlib import Path

plugindir = Path.absolute(Path(__file__).parent)
paths = (".", "lib", "plugin")
sys.path = [str(plugindir / p) for p in paths] + sys.path

from flowlauncher import FlowLauncher 
import os
import xml.etree.ElementTree as ET
import re


class SteamAccountSwitcher(FlowLauncher):

    # query is default function to receive realtime keystrokes from wox launcher
    def query(self, query):
        results = []
        steam_profiles = []
        xml_path = os.path.expandvars(r"%appdata%\TcNo Account Switcher\LoginCache\Steam\VACCache")
        avatar_path = os.path.expandvars(r"%appdata%\TcNo Account Switcher\wwwroot\img\profiles\steam")
        for file in os.listdir(xml_path):
            if file.endswith(".xml"):
                file_path = os.path.join(xml_path, file)
                tree = ET.parse(file_path)
                profile = tree.getroot()
                steamId64 = profile.find("steamID64").text
                steam_profiles.append({
                    "steamId": profile.find("steamID").text,
                    "steamId64": steamId64,
                    "avatarIcon": os.path.join(avatar_path, steamId64 + ".jpg"),
                })
        for stm in steam_profiles:
            if not re.search(query, stm["steamId"], re.IGNORECASE):
                continue
            results.append({
                "Title": stm["steamId"],
                "SubTitle": stm["steamId64"],
                "IcoPath": stm["avatarIcon"],
                "JsonRPCAction": {
                    "method": "switch",
                    "parameters": [stm["steamId64"]],
                    "dontHideAfterAction": False
                }
            })
        return results

    def switch(self, steamId64):
        folder = "C:/Program Files/TcNo Account Switcher/"
        cmd = (
            f'cd "{folder}" && "TcNo-Acc-Switcher.exe" "+s:{steamId64}"'
        )
        os.system(cmd)
        return None

if __name__ == "__main__":
    SteamAccountSwitcher()
