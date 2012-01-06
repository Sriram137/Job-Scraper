import twitter, sys, re, requests, BeautifulSoup
from collections import Counter
twitterURL = 'http://twitter.com'

def fetch(user):
    data = {}
    api = twitter.Api()
    max_id = None
    total = 0
    while True:
        try:
            statuses = api.GetUserTimeline(user, count=200, max_id=max_id)
        except Exception:
            break
        newCount = ignCount = 0
        for s in statuses:
            if s.id in data:
                ignCount += 1
            else:
                data[s.id] = s
                newCount += 1
        total += newCount
        print >> sys.stderr, "Fetched %d /%d / %d new/old/total." % (
            newCount, ignCount, total)
        if newCount == 0:
            break
        max_id = min([s.id for s in statuses]) - 1
    return data.values()

def html_to_text(data):
    soup = BeautifulSoup.BeautifulSoup(data)
    [x.extract() for x in soup.findAll('script')]
    [x.extract() for x in soup.findAll('style')]
    soup1 = soup.body
    content = ""
    if soup1:
        content = ''.join(soup1.findAll(text=True))
    return content

stat = fetch("fredwilson")
updates = []
C = Counter()
L = Counter()
T = Counter()
invalid_words = ":),:(,:d,:p,?,:/,rt,good,begin,links,comment,terms,facebook,months,years,set,o,cancel,vcard,photos,status,cancel,sumbit,click,reset,o,terms,posted,blog,twitter,tweet,html,body,title,google,contact,thanks,going,need,perv,next,shareremoveflag,videos,added,privacy,fm,login,register,registar,link,added,queue,want,back,know,much,reply,things,lists,working,days,views,user,video,photo,click,userunblock,tarcking,tag,open,watching,blog,spamblock,twitpic,liked,rectangle,zone,content,pixel,medium,sitemeter,watching,asked,filter,comments,footer,tagalways,more,a,a,able,now,really,out,about,across,after,all,almost,also,am,among,an,and,any,are,as,at,be,because,been,but,by,can,cannot,could,dear,da,did,do,does,either,else,ever,every,for,from,get,got,had,has,have,he,her,hers,him,his,how,however,i,if,in,into,is,it,its,just,least,let,like,likely,may,me,might,most,must,my,neither,no,nor,not,of,off,often,on,only,or,other,our,own,rather,said,say,says,she,should,since,so,some,suck,sucks,than,that,the,their,them,then,there,these,they,this,tis,to,too,twas,u,us,wants,was,we,were,what,when,where,which,while,who,whom,why,will,with,would,work,year,yet,you,your".split(",")
x = open("common_word_list").read().strip().split(",")
invalid_words.extend(x)
invalid_words = set(invalid_words)
b,v = 0, 0
for x in stat:
    t = x.text
    urls = ""
    if b<100:
        urls = re.findall("(?P<url>https?://[^\s]+)", t)
    for url in urls:
        try:
            content = html_to_text(requests.get(url).content)
            b += 1
            print "B ",b
            for y in content.split():
                if y.lower() not in invalid_words and y[0]!='@' and y.isalpha():
                    L[y.lower()] += 1
        except Exception:
            pass
    for y in t.split():
        if y.lower() not in invalid_words and y[0]!='@' and y.isalpha():
            C[y.lower()] += 1
        if y[0] == "#":
            C[y[1:].lower()] += 10
            T[y[1:].lower()] += 1
    v +=1
    if v>700:
        break
    print "V ",v
print "From Tweets"
print C.most_common(18)
print "From Tags"
print T.most_common(18)
print "From Links"
print L.most_common(18)
print "Links Processed"
print b
