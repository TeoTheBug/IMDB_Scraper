import requests
import time
from bs4 import BeautifulSoup as bs
import re

base_url = "https://www.imdb.com/title/tt2861424/episodes/?season="
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
quantita_stagioni = 7

class episode:
    def __init__(self):
        self.season = 0
        self.number = 0
        self.mark = 0
        self.title = ""
    def __str__(self):
        return f"[{self.mark}]  S{self.season} E{self.number} {self.title}"

for i in range(quantita_stagioni):
    print("Getting: " + base_url + str(i+1))
    result = requests.get(f"{base_url}" + str(i+1), headers=headers)
    if result.status_code == 200:
        with open(f"season_{i}.html", "wb+") as f:
            f.write(result.content)
        time.sleep(1)
print("done")

title_pattern = r"S(\d+)\.E(\d+) ∙ (.+)"

episodes=[]

for i in range(quantita_stagioni):
    fname = f"season_{i}.html"
    with open(fname, "r", encoding="utf-8") as f:
        page = f.read()
        soup = bs(page, features="html.parser")
        
        title_tags = soup.find_all("div", {"class":"ipc-title__text"})

        mark_tags = soup.select('span[aria-label]')

        for title, mark  in zip(title_tags, mark_tags):
            # title
            match_t = re.match(title_pattern, title.get_text())
            if match_t:
                season = int(match_t.group(1))
                ep_num = int(match_t.group(2))
                title = match_t.group(3)
                #print(season,ep_num,title,end="")
            #else:
            #    print("No match found.")

            temp = mark.get_text().strip().split("/")
            mark = temp[0]
            #print(mark)

            e = episode()
            e.season=season
            e.number=ep_num
            e.title=title
            e.mark=mark

            episodes.append(e)

sorted_by_mark = sorted(episodes, key=lambda x: x.mark, reverse=reversed)
for e in sorted_by_mark:
    print(e)
