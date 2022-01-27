from bs4 import BeautifulSoup
import requests
import csv
import constant
import time


def get_commit_fequency(repo_link, user):
    req = requests.get(f"{constant.USER_URL}{repo_link}{constant.COMMIT_URL}", headers={'User-Agent': "Magic Browser"})
    print(f"{constant.USER_URL}{repo_link}{constant.COMMIT_URL}")
    soup = BeautifulSoup(req.content, "html.parser")
    dates = soup.find_all('div', {'class', 'TimelineItem-badge'})
    numbers_of_commits = soup.find_all('div', {'class', 'flex-auto min-width-0'})
    try:
        return len(dates) / (len(numbers_of_commits) - 1)
    except ZeroDivisionError:
        return 0


def get_repo(user):
    req = requests.get(f"{constant.USER_URL}{user}{constant.REPO_URL}", headers={'User-Agent': "Magic Browser"})
    soup = BeautifulSoup(req.content, "html.parser")
    repositories = soup.find_all('div', {'class', 'col-10 col-lg-9 d-inline-block'})
    print(len(repositories))
    repositories_details = {}
    for repo in repositories:
        if repo:
            repo_link = repo.find('a', href=True)
            avr_frequency = get_commit_fequency(repo_link['href'], user)
            repositories_details['REPOSITORY_NAME'] = repo.a.string
            repositories_details['AVERAGE_COMMITS'] = avr_frequency
    return repositories_details


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
    return user_details


def get_details(user):
    user_details = {}
    user_name = user.find('a', {'class', 'color-fg-muted'})
    try:
        user_name = user_name.em.string
        user_details.update(get_repo(user_name))
        print(user_details)
    except AttributeError:
        return
    name = user.find('div', {'class', 'f4 text-normal'}).a.text.strip()
    bio = user.find('p', class_='mb-1')

    user_details['NAME'] = name
    user_details['BIO'] = bio
    if bio:
        user_details['BIO'] = bio.text.strip()
    else:
        user_details['BIO'] = None
    time.sleep(5)
    user_details.update(get_user_details(user_name))
    print(user_details)
    return user_details


def scraper(name):
    fields = ['NAME', 'USER_NAME', 'BIO', 'FOLLOWERS', 'REPOSITORIES', 'REPOSITORY_NAME', 'AVERAGE_COMMITS']
    out_file = open('scraped_data.csv', 'w')
    csvwriter = csv.DictWriter(out_file, delimiter=',', fieldnames=fields)
    user_data = {}
    page_no = 0
    while True:

        if page_no > 10:
            break

        url = f"{constant.BASE_URL}{page_no}{constant.ATTRIBUTE1}{name}{constant.SEARCH_TYPE}"
        req = requests.get(url, headers={'User-Agent': "Magic Browser"})
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
