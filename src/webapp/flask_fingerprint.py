from flask import Flask, render_template, request, jsonify
from database.db_modules import get_data
from database.firebase_modules import upload_to_firebase, download_from_firebase
import json

app = Flask(__name__)


@app.route('/')
def index():

    download_from_firebase('database/Contact_Tracing.db',
                           'webapp/database/Contact_Tracing.db')

    lists = get_data()

    return render_template('index.html', lists=json.dumps(lists))


@app.route('/_array2python')
def array2python():
    wordlist = request.args.get('wordlist', [])
    print(wordlist)
    return jsonify(result=wordlist)


if __name__ == '__main__':

    app.run(host='0.0.0.0', debug=True)
