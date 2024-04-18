from flask import Flask, request, jsonify, render_template, send_from_directory
from google_scraper import *
from organizing_urls import *
from map_values import *
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'archivos'

@app.route('/')
def upload():
    return render_template("sample4.html")


@app.route('/scrape', methods=['POST'])
def scrape_data():
    try:
        data = request.json
        query_input = data["query"]
        qoption_input = data["qoption"]
        qexception_input = data["qexception"]
        qrangedate_input = data["qrangedate"]
        qsite_input = data["qsite"]
        nqueries_input = data["nqueries"]
        
        
        if not os.path.exists('archivos'):
           os.makedirs('archivos')

        file_path = asyncio.run(main(nqueries=nqueries_input, query=query_input, qoption=qoption_input, qexception=qexception_input, qrangedate=qrangedate_input, qsite=qsite_input))
        
        return jsonify({'message': 'Scraping successful!', 'output_file': file_path})
    
    except Exception as e:
        return jsonify({'error scrape': str(e)})


@app.route('/visualize', methods=['GET'])
def visualize_data():

    try:
        data = asyncio.run(states())
        return jsonify({'message': 'Organizing succesful!', 'Data': data})
    
    except Exception as e:
        return jsonify({'error visualize': str(e)})
  

@app.route('/download', methods=['GET'])
def download_results():
    try:       

        return send_from_directory(app.config['UPLOAD_FOLDER'], 'dict_news.json', as_attachment=True)

    except Exception as e:
        return jsonify({'error download': str(e)})
    
@app.route('/table', methods=['GET'])
def table_data():
    try:       
        return send_from_directory(app.config['UPLOAD_FOLDER'], 'links.json', as_attachment=True)
    
    except Exception as e:
        return jsonify({'error table': str(e)})

if __name__ == '__main__':
    app.run(debug=True)  
