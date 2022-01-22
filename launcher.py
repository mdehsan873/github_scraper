import git_scraper

name = input("Enter Query\n")
while True:
    if name:
        name = name.replace(' ', '+')
        git_scraper.scraper(name)
    else:
        print("Enter Valid Input")
