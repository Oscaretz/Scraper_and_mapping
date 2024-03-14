import aiohttp
import pandas as pd
import asyncio
import json
import time
from bs4 import BeautifulSoup

class MexicanStatesScraper:
    def __init__(self, mexican_states):
        self.mexican_states = mexican_states
        self.state_urls_dict = {}

    async def fetch_page(self, session, url):
        async with session.get(url) as response:
            return await response.text()

    async def check_for_mexican_states(self, session, url_data, Title, Source, Date):
        html_content = await self.fetch_page(session, url_data['Link'])
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract the info from the page
        page_text = soup.get_text()

        # Verify if the page contains some Mexican state
        found_states = [state for state in self.mexican_states if state.lower() in page_text.lower()]
        return found_states, Title, url_data['Link'], Source, Date

    async def process_url(self, session, Title, url_data):
        found_states, Title, url, Source, Date = await self.check_for_mexican_states(session, url_data, Title, url_data['Source'], url_data['Date'])

        # Collecting the URLs found per state in the dictionary
        for state in found_states:
            if state not in self.state_urls_dict:
                self.state_urls_dict[state] = []
            self.state_urls_dict[state].append({"Link": url, "Title": Title, "Source": Source, "Date": Date})

    async def process_urls(self, url_data):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=20)) as session:
            tasks = [self.process_url(session, Title, data) for Title, data in url_data.items()]
            await asyncio.gather(*tasks)

    def save_to_json(self):
        with open('organized_URLs.json', 'w') as json_file:
            json.dump(self.state_urls_dict, json_file, indent=5)
            print('*****Results saved to estado_results22.json*****')

    def save_to_dataframe(self):
        df = pd.DataFrame.from_dict(self.state_urls_dict, orient='index')
        df.to_csv('organized_URLs.csv', index_label='Index')
        print('*****Results saved to organized_URLs.csv*****')

async def main():
    # Load URLs from a JSON file
    with open('scraper_results.json', 'r', encoding='utf-8') as json_file:
        url_data = json.load(json_file)

    if not url_data:
        print("Error: URLs not found in JSON file.")
        return

    mexican_states = ["Aguascalientes", "Baja California", "Baja California Sur", "Ciudad de México", "Campeche", "Chiapas", "Chihuahua", "Coahuila", "Colima", "Durango", "Guanajuato", "Guerrero", "Hidalgo", "Jalisco", "Estado de México", "Michoacán", "Morelos", "Nayarit", "Nuevo León", "Oaxaca", "Puebla", "Querétaro", "Quintana Roo", "San Luis Potosí", "Sinaloa", "Sonora", "Tabasco", "Tamaulipas", "Tlaxcala", "Veracruz", "Yucatán", "Zacatecas"]

    scraper = MexicanStatesScraper(mexican_states)
    await scraper.process_urls(url_data)
    scraper.save_to_dataframe()

# Executing the loop of events of asyncio
start = time.time()
asyncio.run(main())
end = time.time()
print(f'TIME: {end - start}')
