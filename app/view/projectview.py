from flask import render_template

from app import app

@app.route('/plistView/', methods=['GET'])
def plistView():
    return render_template('projectview/plistView.html')
