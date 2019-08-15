#! python3
import re, urllib.request, csv

emailRegex = re.compile(r'''
#example :
#something-.+_@somedomain.com
(
([a-zA-Z0-9_.+]+
@
[a-zA-Z0-9_.+]+)
)
''', re.VERBOSE)
        
#Extacting Emails
def extractEmailsFromUrlText(urlText, comp_name):
    extractedEmail =  emailRegex.findall(urlText)
    allemails = []
    for email in extractedEmail:
        allemails.append(email[0])
    lenh = len(allemails)
    print("\tNumber of Emails : %s\n"%lenh )
    seen = set()
    for email in allemails:
        if email not in seen:  # faster than `word not in output`
            seen.add(email)
            if ("com" in str(email)) or ("org" in str(email)):
                with open(file_out, 'a') as writeFile:
                    row = str(email)+ ", " + comp_name + "\n"
                    writeFile.write(row)

#HtmlPage Read Func
def htmlPageRead(url, comp_name):
    try:
        headers = { 'User-Agent' : 'Mozilla/5.0' }
        request = urllib.request.Request(url, None, headers)
        response = urllib.request.urlopen(request)
        urlHtmlPageRead = response.read()
        urlText = urlHtmlPageRead.decode()
        extractEmailsFromUrlText(urlText, comp_name)
    except:
        pass
    
#EmailsLeechFunction
def emailsLeechFunc(url, comp_name):
    
    try:
        htmlPageRead(url, comp_name)
    except urllib.error.HTTPError as err:
        if err.code == 404:
            try:
                url = 'http://webcache.googleusercontent.com/search?q=cache:'+url
                htmlPageRead(url, comp_name)
            except:
                pass
        else:
            pass    
      
# TODO: Open a file for reading urls
            
contacts = {}

file_in = "contacts.csv"
file_out = "comp_info.csv"

with open(file_in) as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    for row in csvReader:
        comp_name = str(row[1])
        comp_url = str(row[0])
        
        emailsLeechFunc(comp_url, comp_name)
        
        




