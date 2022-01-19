import git_scraper as git
name=input("Enter name you want to  get data\n")
if name:
    name=name.replace(' ','+')
    git.scraper(name)
else:
    print("Enter Valid Input")