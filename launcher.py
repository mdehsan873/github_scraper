import git_scraper

name = input("Enter Query\n")
if name:
    name = name.replace(' ', '+')
    git_scraper.scraper(name)
else:
    print("Enter Valid Input")
