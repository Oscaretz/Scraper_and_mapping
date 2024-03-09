import aiohttp
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

    async def check_for_mexican_states(self, session, url, Title):
        html_content = await self.fetch_page(session, url)
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract the info from the page
        page_text = soup.get_text()

        # Verify if the page contains some Mexican state
        found_states = [state for state in self.mexican_states if state.lower() in page_text.lower()]
        return found_states, Title

    async def process_url(self, session, Title, data):
        url = data.get('Link')
        found_states, Title = await self.check_for_mexican_states(session, url, Title)

        # Collecting the URLs found per state in the dictionary
        for state in found_states:
            if state not in self.state_urls_dict:
                self.state_urls_dict[state] = []
            self.state_urls_dict[state].append({"Link": url, "Title": Title})

    async def process_urls(self, url_data):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=10)) as session:
            tasks = [self.process_url(session, Title, data) for Title, data in url_data.items()]
            await asyncio.gather(*tasks)

    def save_to_json(self):
        with open('organized_URLs.json', 'w') as json_file:
            json.dump(self.state_urls_dict, json_file, indent=3)
            print('*****Results saved to estado_results22.json*****')

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
    scraper.save_to_json()

# Executing the loop of events of asyncio
start = time.time()
asyncio.run(main())
end = time.time()
print(f'TIME: {end - start}')
