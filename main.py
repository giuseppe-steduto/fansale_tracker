"""
Author: Giuseppe Steduto

This script is intended to be constantly run to check the availability of concert tickets on FanSale (by Ticketone)
that meet the specified criteria
"""
import requests as requests
import selenium as s
import bs4

def check_url(u):
    if u == "":
        return False
    return True

def print_cookies(cj):
    for cookie in cj:
        print(cookie.name, end=" - ")
    print("\n")


URL = "https://www.fansale.it/fansale/tickets/pop-amp-rock/pinguini-tattici-nucleari/558153/13359444"

# Input and check URL
URL_INPUT = ""
while not check_url(URL_INPUT):
    URL_INPUT = input("Insert the complete Fansale input of the event you want to bui tickets for: ")


# Extract the ticket list from the website
headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"} #Change UA
response_challenge_validator = requests.get(URL, headers=headers)
cookies = response_challenge_validator.cookies
print("Prima richiesta: ", end="")
print_cookies(cookies)

res_challenge_validator3 = requests.get("https://www.fansale.it/_sec/cp_challenge/ak-challenge-3-6.htm", headers=headers, cookies=cookies.get_dict())
cookies.update(res_challenge_validator3.cookies)
print("Dopo aver fatto richiesta a ak-challenge: ", end="")
print_cookies(cookies)

res_challenge_validator4_verify = requests.get("https://www.fansale.it/_sec/cp_challenge/verify", headers=headers, cookies=cookies.get_dict())
# cookies.update(res_challenge_validator4_verify.cookies)
print("Dopo aver fatto richiesta a verify: ", end="")
print_cookies(cookies)

# TODO aggiornare i cookie con quelli che vengono richiamati dall'XHR con il JS che viene inviato in ak-challenge

res = requests.get(URL, headers=headers, cookies=cookies.get_dict())
print("Inviati per la richiesta finale: ", end="")
print_cookies(cookies)
print("************")
print(res.content)

"""
soup = bs4.BeautifulSoup(response.content, 'html.parser')
rev_div = soup.findAll("div", attrs={"class", "EventEntry"})
"""
