import urllib, urllib2, sys
from BeautifulSoup import BeautifulSoup

def get_job_list(language, country_code):
    language = urllib.quote(language)
    country_code = urllib.quote(country_code)
    url = "http://www.linkedin.com/jsearch?keywords=%s&searchLocationType=I&countryCode=%s&page_num=1&pplSearchOrigin=MDYS&sortCriteria=R#"% (language, country_code)
    req = urllib2.urlopen(url)
    page = req.read()

    soup = BeautifulSoup(page)

    total_number = soup.find("span", {"class" : "keywords"})
    company_list = soup.findAll('h4')[1].parent.findAll('label')

    final_list = []

    for x in company_list:
        final_list.append(x.contents)
    return (final_list[1:-1], total_number)

def go():
    language = "Python"
    country_code = "us"
    if len(sys.argv) == 3:
        language = sys.argv[1]
        country_code = sys.argv[2]


    (lis, total)= get_job_list(language, country_code)
    for x in lis:
        print x[0]
    print
    print "Total: %s"% (total.contents[2].contents[0])
go()
