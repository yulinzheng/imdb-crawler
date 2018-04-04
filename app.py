from flask import Flask
from flask import render_template
import csv
app = Flask(__name__)

def get_csv():
    csv_file = open('./top_1000.csv', 'r') 
    csv_list = list(csv.DictReader(csv_file))
    return csv_list

@app.route('/')
def index():
    csv_list = get_csv()
    return render_template('index.html', object_list=csv_list)

if __name__=='__main__':
    app.run(debug=True, use_reloader=True)
