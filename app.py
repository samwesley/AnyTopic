from flask import Flask
import webpage_question_flow
import new_subscription
import full_process

application = Flask(__name__,)

@application.route('/health')
def health():
    return "OK", 200

@application.route('/web_questions')
def get_topics(category):
    response = webpage_question_flow.category_request(category)
    return response

@application.route('/new_subscription')
def new_subscription(email, category, category_details):
    response = new_subscription.new_subscription(email, category, category_details)
    return "{email} subscribed to {category}".format(email=email, category=category)

@application.route('/run')
def run(email):
    response = full_process.main(email)
    return response


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run(port=80)
