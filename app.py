# -*- coding: utf-8 -*-
import json
import pymorphy2
from flask import Flask, request, render_template
from inflect import PhraseInflector, GRAM_CHOICES

app = Flask(__name__)
app.debug = True

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/inflect", methods=['GET', 'POST'])
def inflect():
    if request.method == 'POST':
        phrases = request.form.getlist('phrase')
        codes = request.form.getlist('code')
        params = dict(zip(codes, phrases))
    else:
        params = request.args

    #if 'phrase' not in params:
    #    return u'укажите слово', 400,  {'Content-Type':'text/plain; charset=utf-8'}
    #if 'forms' not in params and 'cases' not in params :
    #    return u'выберите падежи или/и числа', 400,  {'Content-Type':'text/plain; charset=utf-8'}

    #phrase = params['phrase']
    #form_sets = params.getlist('forms') if params.getlist('forms') else params.getlist('cases')
    form_sets = ['gent', 'accs']

    result = {}
    for (code, phrase) in params.items():
        morph = pymorphy2.MorphAnalyzer()
        inflector = PhraseInflector(morph)
        result2 = {'orig': phrase}
        for forms_string in form_sets:
            form_set = set(forms_string.split(',')) & set(GRAM_CHOICES)
            result2[forms_string] = inflector.inflect(phrase, form_set)
        result[code] = result2
    return json.dumps(result), 200, {'Content-Type':'text/json; charset=utf-8'}

if __name__ == "__main__":
    app.run()
