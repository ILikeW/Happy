import requests
import os
from bs4 import BeautifulSoup as bs


def get_gogo_cookie(email, password):
    s = requests.session()
    animelink = "https://gogoanime3.co/login.html"
    response = s.get(animelink)
    response_html = response.text
    soup = bs(response_html, "html.parser")
    source_url = soup.select('meta[name="csrf-token"]')
    token = source_url[0].attrs["content"]

    data = f"email={email}&password={password}&_csrf={token}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 9; vivo 1916) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36",
        "authority": "gogo-cdn.com",
        "referer": f"https://gogoanime3.co/",
        "content-type": "application/x-www-form-urlencoded",
    }
    s.headers = headers

    r = s.post(animelink, data=data, headers=headers)

    if r.status_code == 200:
        s.close()
        print("Gogoanime cookie generated successfully")
        return s.cookies.get_dict().get("auth")


# Get email and password from environment variables
email = os.environ.get('GOGO_EMAIL')
password = os.environ.get('GOGO_PASSWORD')

if email and password:
    with open("gogoCookie.txt", "w") as f:
        cookie = get_gogo_cookie(email, password)
        if cookie:
            f.write(cookie)
        else:
            print("Failed to generate cookie")
else:
    print("Email or password not provided in environment variables")
