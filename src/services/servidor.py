
import os
from flask import Flask, request, render_template, make_response
import joblib

app = Flask(__name__, static_url_path ='/static')
model = joblib.load('./notebooks/model.pkl')

@app.route('/')
def display_quit():
    return 'Hello Word!' 
    #render_template('template.html')

@app.route('/teste', methods=['GET'])
def teste():
    print('Teste api')
    return 'Teste rota api'

if __name__ == "__main__":
    port = int(os.environ.get('PORT',5500))
    app.run(host='0.0.0.0', port=port)