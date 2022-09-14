
from flask import Flask,request,jsonify
import spacy
import stanza

nlp2 = stanza.Pipeline()
nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)

@app.route("/spacy",methods=["POST"])
def spacy_api():
    results = {}
    pos = {}
    svp = {}
    input_text = request.get_json(force=True)
    doc = nlp(input_text['text'])
    for token in doc:
        pos[token.text] = spacy.glossary.explain(token.tag_)
        if token.dep_ == 'nsubj' :
            svp['subject'] = token.text
        if token.dep_ == 'dobj' :
            svp['object'] = token.text
        if token.dep_ == 'ROOT' : 
            svp['verb'] = token.text
    results['POS'] = pos
    results['svp'] = svp
    return jsonify({'result':results})

@app.route("/corenlp",methods=['POST'])
def corenlp_api():
    results = {}
    pos = {}
    svp = {}
    input_text = request.get_json(force=True)
    doc = nlp2(input_text['text'])
    for sent in doc:
        for word in sent.text:
            pos[word.text] = spacy.glossary.explain(word.pos)
            if word.dep == 'nsubj' :
                svp['subject'] = word.text
            if word.dep == 'dobj' :
                svp['object'] = word.text
            if word.dep == 'ROOT' : 
                svp['verb'] = word.text
    results['POS'] = pos
    results['svp'] = svp
    return jsonify({'result':results})
