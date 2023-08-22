import json
import os
from flask import Flask, render_template, request, session, url_for, redirect
from werkzeug.utils import secure_filename
from analysis import processing
import plotly
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.secret_key = "ewwrtyvjbjh12345fgvn134"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    file_path = session.get('uploaded_data_file_path', None)
    if file_path:
        analysis = processing.ProcessData(file_path)
        values = {"total_revenue": analysis.get_total_revenue(),"average_price_per_item":analysis.average_price_per_item(),
                  "total_orders_count": analysis.get_orders_count(), "total_profit": analysis.get_total_profit(),
                  "best_selling_product": json.dumps(analysis.best_selling_product(),
                                                     cls=plotly.utils.PlotlyJSONEncoder),
                  "top_profitable_products": json.dumps(analysis.top_profitable_products(),
                                                        cls=plotly.utils.PlotlyJSONEncoder),
                  "sales_profit_timeline": json.dumps(analysis.sales_profit_timeline(),
                                                     cls=plotly.utils.PlotlyJSONEncoder),
                  "sales_profit_by_customer_segment": json.dumps(analysis.sales_profit_by_customer_segment(),
                                                      cls=plotly.utils.PlotlyJSONEncoder),
                  "top_profitable_cites": json.dumps(analysis.top_profitable_cites(),
                                                      cls=plotly.utils.PlotlyJSONEncoder),
                  "sales_category_wise": json.dumps(analysis.sales_category_wise(),
                                                      cls=plotly.utils.PlotlyJSONEncoder),
                  }
        return render_template('dashboard.html', values=values)
    else:
        return render_template('upload.html')


@app.route('/upload')
def upload():
    return render_template('upload.html')


@app.route('/uploadFile', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        try:
            f = request.files.get('dataSet')
            data_filename = secure_filename(f.filename)
            data_filename = datetime.now().strftime("%Y%m%d-%H%M%S") + data_filename
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], data_filename))
            session['uploaded_data_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], data_filename)
            return redirect(url_for('dashboard'))
        except Exception as e:
            print(e)
    return redirect(url_for('upload'))


if __name__ == "__main__":
    app.run(debug=True, port=8000)
