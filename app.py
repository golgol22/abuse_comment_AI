from flask import Flask, render_template, request
from service import Service
s = Service()

app = Flask(__name__)

@app.route('/') 
def root():
    return render_template('index.html')

@app.route('/abuse-test', methods=['POST'])  
def abuse_test():
    text = request.form['comment']
    type1 = s.predict_test(text)
    result = text + ': ' + type1
    print(result)
    return render_template('index.html', result=result)

if __name__=='__main__':
    app.run()
