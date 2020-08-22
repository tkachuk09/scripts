import requests
from datetime import datetime, timedelta
headers = {
    'Authorization': 'Bearer zw7xEyIpnpwN6Zwgd3zzk2oKl5zVjDnA',
    'Accept': 'application/json',
    'Content-Type': 'application/json',
}

# Authorization via API key to DNSIMPLE

response1 = requests.get('https://api.dnsimple.com/v2/60591/domains', headers=headers)
response1ToJson = response1.json()

# Get a "total page" output

page = int(response1ToJson['pagination']['total_pages'])  # substitute the number from "total pages" in the cycle
domains = []
i = 1             # make an iteration and cycle below
while i < page:
    spage = str(i)
    response = requests.get('https://api.dnsimple.com/v2/60591/domains?page=' + spage + '&per_page=100/whois_privacy', headers=headers)
    i+=1
    responseToJson = response.json()
    parseJsonToData = responseToJson['data']
    for date in parseJsonToData:
        name = date['name']
        if str(name).endswith(".io"):                   # cycle for skip invalid domains (.io , .co.uk)
            print("Invalid to check domain: " + name)
            if str(name).endswith(".co.uk"):
                print("Invalid domain to check: " + name)
        else:
            domains.append(date['name'])
print("Count of all domains: " + str(len(domains)))  # number of all domains
for d in domains:
    response1 = requests.get('https://api.dnsimple.com/v2/60591/registrar/domains/' + d + '/whois_privacy', headers=headers)
    response1ToJson = response1.json()
    parseData = response1ToJson['data']
    date = parseData["expires_on"]
    # parse "expires_on" data above
    # create a proper condition below
    if date is not None:
        if(datetime.strptime(date, "%Y-%m-%d") - timedelta(days=30)).date() <= datetime.now().date():
            response5 = requests.post("https://api.dnsimple.com/v2/60591/registrar/domains/" + d + "/whois_privacy/renewals", headers=headers)
            print("Domain: " + d + " was successfully renew | old date was: " + date)

            # renew whois_privacy for all domains which expires in <=30 days

print("Finished renew!")

# Successfully renewed all domains