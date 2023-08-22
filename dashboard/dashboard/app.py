import json
import os
from flask import Flask, render_template, request, session
from werkzeug.utils import secure_filename
from analysis import processing
import plotly

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.secret_key = "ewwrtyvjbjh12345fgvn134"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return render_template('dashboard.html')


@app.route('/dashboard')
def dashboard():
    file_path = session['uploaded_data_file_path']
    analysis = processing.ProcessData(file_path)
    values = {"total_revenue": analysis.get_total_revenue(),
              "total_orders_count": analysis.get_orders_count(), "total_profit": analysis.get_total_profit(),
              "best_selling_product" : json.dumps(analysis.best_selling_product(), cls=plotly.utils.PlotlyJSONEncoder)}
    return render_template('dashboard.html', values=values)


@app.route('/upload')
def upload():
    return render_template('upload.html')


@app.route('/uploadFile', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files.get('dataSet')
        data_filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], data_filename))
        session['uploaded_data_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], data_filename)
        return render_template('index.html')
    return render_template("upload.html")


if __name__ == "__main__":
    app.run(debug=True, port=8000)
