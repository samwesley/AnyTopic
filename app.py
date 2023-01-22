from flask import Flask
import webpage_question_flow

application = Flask(__name__,)

@application.route('/health')
def health():
    return "OK", 200

@application.route('/gpt')
def get_topics(category):
    response = webpage_question_flow.category_request(category)
    return response


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run(port=80)
