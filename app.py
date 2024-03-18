from flask import Flask, request, jsonify, render_template
from google_scraper import *
from organizing_urls import *
from map_values import *

app = Flask(__name__)

@app.route('/')
def upload():
    return render_template("sample3.html")

@app.route('/scrape', methods=['POST'])
def scrape_data():
    try:
        data = request.json
        query_input = data["query"]
        year_input = data["year"]
        # Executing the web scraper 
        r =  scraper(num_pages=10, year=year_input, query=query_input)
        return jsonify({'message': 'Scraping successful!', 'results': r})
    
    except Exception as e:
        return jsonify({'error': str(e)})

    # Here you would implement the scraping logic
    # For now, let's just return a message indicating success
    #return jsonify({'message': 'Scraping successful!'})

@app.route('/visualize', methods=['GET'])
def visualize_data():

    try:
        scrape_input = 0
        r = DataMaps(scrape_input)
        return r
    
    except Exception as e:
        return jsonify({'error': str(e)})

    # Here you would implement the data visualization logic
    # For now, let's just return a message indicating success
    #return jsonify({'message': 'Visualization successful!'})

'''@app.route('/download', methods=['GET'])
def download_results():
    # Here you would implement the data download logic
    # For now, let's just return a message indicating success
    #return jsonify({'message': 'Download successful!'})'''

if __name__ == '__main__':
    app.run(debug=True)  # Run the server in debug mode
