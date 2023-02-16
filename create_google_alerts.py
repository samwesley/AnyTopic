import time
from google_alerts import GoogleAlerts
from dotenv import load_dotenv
import os
load_dotenv()

pword = os.getenv("ALERTS_PASSWORD")
# Create an instance

ga = GoogleAlerts('alerts.anytopic@gmail.com', pword)

# Authenticate your user
ga.authenticate()

def create_alerts(category_name):
    print(ga.list())
    RSSlist =  ga.list()
    for i in RSSlist:
        if i['term'] == category_name:
            print(f"{category_name} alert already exists")
            return i['rss_link']
    # Add a new monitor
    print("Creating alert for " + category_name)
    request = ga.create(category_name, {'delivery': 'RSS', 'monitor_match': 'BEST'})
    print("REQUEST: " + str(request))
    if request == []:
        print("error! request empty")
        return None
    else:
        for i in request:
            link = i["rss_link"]
            print(link)
        return link

