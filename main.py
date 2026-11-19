import requests
from bs4 import BeautifulSoup
import smtplib
import os
from dotenv import load_dotenv


load_dotenv()

USER_NAME=os.environ.get("USER_NAME")
PASSWORD=os.environ.get("PASSWORD")
FROM_EMAIL=os.environ.get("FROM_EMAIL")
TO_EMAIL=os.environ.get("TO_EMAIL")

# Full headers would look something like this
header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-GB,de;q=0.8,fr;q=0.6,en;q=0.4,ja;q=0.2",
    "Dnt": "1",
    "Priority": "u=1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Sec-Gpc": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) Gecko/20100101 Firefox/126.0",
}

practice_url = "https://appbrewery.github.io/instant_pot/"
response = requests.get(practice_url, headers=header)
response.raise_for_status()


# 2. Pass response.text (the HTML string) into BeautifulSoup, not the URL
soup = BeautifulSoup(response.text, "html.parser")
# print(soup.get_text())

# Extract the price ($99.99 -> 99.99 as a float)
price_whole = soup.find(class_="a-price-whole").get_text()
price_fraction = soup.find(class_="a-price-fraction").get_text()
price_as_float = float(f"{price_whole}{price_fraction}")

# print(price_as_float)  # Output: 99.99

title = soup.find(id="productTitle").get_text().strip()
# print(title)

# Set the price below which you would like to get a notification
BUY_PRICE = 100

if price_as_float < BUY_PRICE:
    message = f"{title} is on sale!"

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=USER_NAME, password=PASSWORD)
        connection.sendmail(
            from_addr=FROM_EMAIL,
            to_addrs=TO_EMAIL,
            msg=f"Subject:Amazon Price Alert!\n\n{message}\n{practice_url}".encode("utf-8")
        )
    print("Mail sent successfully.")
        
else:
    print(f"Price not changed!!!")