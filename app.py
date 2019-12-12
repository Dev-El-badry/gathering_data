from flask import Flask, render_template, url_for, redirect, request
from flask import Flask, render_template, session, redirect, url_for,flash
from flask_wtf import FlaskForm
from flask_jsglue import JSGlue
from Project import Project

app = Flask(__name__)
jsglue = JSGlue(app)


app.config['SECRET_KEY'] = 'mykey'


@app.route('/', methods=['GET', 'POST'])
def index() :

    if request.method == 'POST' :
        item_search = request.values.get('word_search')

        Project(item_search)
        
        return 'well done'
        


    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
