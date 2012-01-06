import requests, BeautifulSoup

all_words = list()
for i in xrange(0,29,2):
    ii = "%02d"%(i+1)
    ij = "%02d"%(i+2)
    url = "".join(["http://www.paulnoll.com/Books/Clear-English/words-",ii,"-",ij,"-hundred.html"])
    # print url
    r = requests.get(url).content
    soup = BeautifulSoup.BeautifulSoup(r)
    r = soup.findAll("li")

    for x in r:
        all_words.append(x.string.strip())

print ",".join(all_words)
