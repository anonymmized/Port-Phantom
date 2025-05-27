import os
import requests

url = "https://standards-oui.ieee.org/oui.txt "
response = requests.get(url)
if os.path.exists("oui.txt"):
    print("oui.txt is already exists")
else:
    with open("oui.txt", "wb") as f:
        f.write(response.content)
        print("[+] База OUI успешно скачана!")