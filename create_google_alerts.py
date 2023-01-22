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
    # Add a new monitor
    print("Creating alert for " + category_name)
    request = ga.create(category_name, {'delivery': 'RSS', 'monitor_match': 'BEST'})
    for i in request:
        link = i["rss_link"]
        print(link)
        time.sleep(1)
    return link

