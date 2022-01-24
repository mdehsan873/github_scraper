from bs4 import BeautifulSoup
import urllib
import requests
import csv
import constant
import time


def get_user_details(user):
    req = requests.get(constant.USER_URL + user, headers={'User-Agent': "Magic Browser"})
    soup = BeautifulSoup(req.content, "html.parser")

    user_details = {}
    repositories = soup.find('nav', {'class', 'UnderlineNav-body width-full p-responsive'}).span.text
    try:
        followers = soup.find('div', {'class', 'flex-order-1 flex-md-order-none mt-2 mt-md-0'}).span.text
        user_details['FOLLOWERS'] = followers
        user_details['REPOSITORIES'] = repositories
    except AttributeError:
        print(constant.ERROR)
    return save_details


def get_details(user):
    user_name = user.find('a', {'class', 'color-fg-muted'})
    try:
        user_name = user_name.em.string
    except AttributeError:
        return
    name = user.find('div', {'class', 'f4 text-normal'}).a.text.strip()
    bio = user.find('p', class_='mb-1')

    save_details = {'NAME': name, 'USER_NAME': user_name}
    if bio:
        save_details['BIO'] = bio.text.strip()
    else:
        save_details['BIO'] = constant.BIO
    time.sleep(5)
    save_details.update(get_user_details(user_name))
    print(save_details)
    return save_details


def scraper(name):
    fields = ['NAME', 'USER_NAME', 'BIO', 'FOLLOWERS', 'REPOSITORIES']
    out_file = open('scraped_data.csv', 'w')
    csvwriter = csv.DictWriter(out_file, delimiter=',', fieldnames=fields)
    user_data = {}
    page_no = 0
    while True:

        if page_no > 10:
            break

        url = f"{constant.BASE_URL}{page_no}{constant.ATTRIBUTE1}{name}{constant.SEARCH_TYPE}"
        req = requests.get(url, headers={'User-Agent': "Magic Browser"})
        # print(req)
        # page = req.get(req)
        soup = BeautifulSoup(req.content, "html.parser")
        users = soup.find_all('div', {'class', 'd-flex hx_hit-user px-0 Box-row'})
        try:
            for user in users:
                user_data = (get_details(user))
                if user_data:
                    csvwriter.writerow(user_data)
            page_no += 1
            time.sleep(5)

        except AttributeError:
            print(constant.ERROR)
            break

    out_file.close()
