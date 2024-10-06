
# Web Scraper & Maping
![alt text](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue) 
![alt text](https://img.shields.io/badge/VSCode-0078D4?style=for-the-badge&logo=visual%20studio%20code&logoColor=white)

## Google News?  📰

Google News is a comprehensive platform for accessing and discovering news articles from around the world. Use it as your go-to source for staying informed about current events and trending topics, or as a tool to delve deeper into specific news categories that interest you.

Google News offers a user-friendly interface that makes it easy to navigate and explore a wide range of news stories. Whether you're looking for breaking news, in-depth analysis, or local updates, Google News provides a platform for grass-roots news discussion and discovery.

### Why Scrape and Map news from Google News? 📈

A web scraper for Google News is a tool designed to automatically extract news articles and related information from the Google News website. Additionally, this tool visualizes a heatmap depicting the trends of the Mexican states. The gathered data can be downloaded in a JSON file, which includes headlines, publication dates, links, and sources. Web scraper news can serve various purposes, such as conducting research on news trends, analyzing media coverage, or aggregating news content for customized news feeds.

This repository houses a robust web scraper developed in Python, which utilizes libraries such as BeautifulSoup and Requests. It enables you to scrape news data from Google News based on specified search parameters and retrieve the results in JSON format. Below are the details on how to set up and utilize this web scraper effectively.

## Dependencies:
We will be using the following dependencies for our code, which will be installed later:

- aiohttp
- asyncio
- bs4
- Flask[async]
- pandas
- fake_useragent
- requests_html
- jsonify


To install them manually, run the next command changing the placeholder value with the name of the required dependency:

```
pip install <placeholder>
```

## Files Included: :pick:	

1. **app.py**: This file contains the Flask application with endpoints for executing the web scrape news, visualizing the data, download results and run the interface on the browser.

2. **Dockerfile**: Dockerfile for building a Docker image to run the Flask application in a containerized environment.

3. **compose.yml**: Docker Compose file for defining and running multi-container Docker applications. It specifies the Flask application service.

4. **requirements.txt**: File listing the Python dependencies required for this application.

5. **sample4.html**: Interface on which the user interacts in order to use all the tools of the program (scrape, visualize and download).

6. **GoogleScraper.py**: Python file for scrape the Google news.

4. **organizing_urls.py**: Python file which organize the news on a json file.


## Setting Up and Running the Application: ⚒️

### Docker Installation:

Before running the application, make sure you have Docker installed on your system. Follow these steps to install Docker:

1. **Download Docker**:
   - Visit the [Docker website](https://www.docker.com/get-started) to download Docker for your operating system.
   - Follow the installation instructions provided for your specific platform.

2. **Verify Installation**:
   - Once Docker is installed, open a terminal or command prompt and run the following command to verify the installation:
     ```
     docker --version
     ```
   - If Docker is installed correctly, you should see the version information displayed in the terminal.

3. **Run Docker Desktop**:
   - Launch Docker Desktop from your applications menu or start menu.
   - Docker Desktop will start the Docker service, allowing you to build and run Docker containers on your system.

Now that Docker is installed, you can proceed with setting up and running the application using the instructions provided below.

### Build and run:
To download the API and initialize it, open the terminal in yout chosen Directory and run the next commands in it:

1. **Clone the Repository**: 
```
git clone https://github.com/Oscaretz/Scraper_and_mapping/
```
This line clone the API from the repository to your machine

2. **Navigate to the Directory**:
```
cd Scraper_and_mapping
```
Open the file you just created

3. **Run the Docker Container**:
```
docker-compose up --build
```
Build and run the container using docker compose

3. **Run the app**:

  Copy the 1st direction (It usually is 127.0.0.1:5000) and paste it in your browser.



## How To Use The Inferface: :tv:

Once you've opened the browser with the given direction, follow these steps to set it up and start scraping:

![alt text](https://github.com/Oscaretz/Scraper_and_mapping/blob/main/ss/front.png?raw=true)

1. **Scrape news**:
   Insert all the parameters you want and click the botom 'Scrape'. After that, the table of the righ side will be filled with 10 news as reference. Here is the guide to write the parameters:

    - Cantidad de noticas (max. 100): _Insert the amount of news to collect, mutiples of 10._

    - Palabra(s) clave: _Insert the main keywords to search, separated by comas. Could be one or more._

    - Rango de fecha: _Optional; Insert the range date to scrape beging with the first date and end with the last date: m1/d1/y1-m2/d2/y2_

    - Palabra(s) restringida(s): _Optional; Insert the restricted words, separated by comas. Could be one or more._

    - Palabra(s) secundaria(s): Optional; _Insert the secundary keywords, separated by comas. Could be one or more._ 

    - Dominio web: _Optional; Insert the domain (ej. www.samplenews.com) or type of domain  (.gov .edu .org .mx .col .eu etc...)_
  ![alt text](https://github.com/Oscaretz/Scraper_and_mapping/blob/main/ss/scrapping.png?raw=true)

2. **Visualize the heat map**: Visualize the heat map with the data gathered by clicking the botom 'Visualize'.
![alt text](https://github.com/Oscaretz/Scraper_and_mapping/blob/main/ss/mapping.png?raw=true)

4. **Downloa results**:
   Click the bottom 'Download' to download a JSON file with the news collected within the given information (Title, source, date, link and State)

```json
{
       "Title": {
        "Source": "",
        "Link": "",
        "Date": "",
        "States": ["", ...] 
    }, 
    ...
}
```


## Notes: 📓

- This web scraper is a simple example with some customization based on the tools that Google Advanced Search provide
- The excessive use of the scrape could cause a temporary ban from Google, in case this happen, just wait a time before doing more queries.

Feel free to modify and expand upon this web scraper according to your requirements. If you encounter any issues or have suggestions for improvements, please don't hesitate to open an issue or pull request. Happy scraping!


