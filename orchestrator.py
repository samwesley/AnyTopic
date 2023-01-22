import create_folders
import mark_duplicates
import news_parse
import slack_app
import get_summary
import get_user_info
import check_for_data
import relevancy_scoring
import gpt_relevancy_scoring
from flask import Flask, request, Response

nickEmail = "nick@urbanriv.org"
samEmail = "samwesley3@gmail.com"
testEmail = "allTest2@gmail.com"


def main(category):
    print("Starting the program for: " + category)
    print(check_for_data.main(category))
    print(news_parse.main(category))
    print(mark_duplicates.main(category))
    print(gpt_relevancy_scoring.main(category))
    print(get_summary.main(category))
    print(slack_app.sendMessages(category, samEmail))

def get_categories(email):
    keys = get_user_info.get_category_keys(email)
    for i in keys:
        main(i)



#main(sys.argv[1])
get_categories(samEmail)
