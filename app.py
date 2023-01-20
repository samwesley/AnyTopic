from flask import Flask

application = Flask(__name__,)

@application.route('/health')
def health():
    return "OK", 200

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run(port=80)