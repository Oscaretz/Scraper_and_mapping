import aiohttp
import asyncio
import json
import time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

class GoogleSearchNews:
    def __init__(self, num_pages, year, query):
        self.num_pages = num_pages
        self.noticias = {}
        self.user_agent = UserAgent()
        self.year = year
        self.query = query

    async def get_info_new(self, session, url):
        async with session.get(url, headers={'User-Agent': self.user_agent.random}) as response:
            try:
                response.raise_for_status()
                soup = BeautifulSoup(await response.text(), 'lxml')
                news_elements = soup.select('a.WlydOe')

                for element in news_elements:
                    source = element.select_one('div.MgUUmf.NUnG9d > span').text.strip()
                    title = element.select_one('div.n0jPhd.ynAwRc.MBeuO.nDgy9d').text.strip()
                    link = element['href']
                    date = element.select_one('div.OSrXXb.rbYSKb.LfVVr > span').text.strip()

                    self.noticias[title] = {'Source': source, 'Link': link, 'Date': date}

            except aiohttp.ClientResponseError as e:
                print(f"Failed to access the page. ClientResponseError: {e}")

    async def get_all_news(self):
        tasks = []
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=10)) as session:
            for page_num in range(1, self.num_pages + 1):
                url = f"https://www.google.com/search?q={self.query.replace(' ','%20')}%C3%B3n&cr=countryMX&sca_esv=67393e17c4183385&hl=es-419&gl=MX&biw=1366&bih=647&tbs=sbd%3A1%2Ccdr%3A1%2Ccd_min%3A{self.year}%2Ccd_max%3A{self.year}%2Cctr%3AcountryMX&tbm=nws&sxsrf=ACQVn08n6MZ5dLUWMKiVtyFXkWoTHss1PA%3A1709841442399&ei=IhzqZaz_F6arur8Pxr-4iAU&ved=0ahUKEwismK_e9-KEAxWmle4BHcYfDlEQ4dUDCA4&uact=5&oq=inundaci%C3%B3n&gs_lp=Egxnd3Mtd2l6LW5ld3MiC2ludW5kYWNpw7NuMggQABiABBixAzIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABEjKJFC8A1ioE3AAeACQAQCYAcUBoAGTEKoBBDEuMTa4AQPIAQD4AQGYAgagArIFwgIFECEYoAHCAgYQABgWGB6YAwCIBgGSBwMwLjagB7Mt&sclient=gws-wiz-news"
                url_final = f"{url}&start={10 * (page_num - 1)}"
                tasks.append(self.get_info_new(session, url_final))

            await asyncio.gather(*tasks)

    def save_to_json(self, output_file):
        with open(output_file, 'w', encoding='utf-8') as json_file:
            json.dump(self.noticias, json_file, indent=8, ensure_ascii=False)
            print(f'*****Results saved to {output_file}*****')

if __name__ == "__main__":
    y, q = "2022", "Inundaciones"
    output_file = 'scraper_results.json'

    inicio = time.time()
    scraper = GoogleSearchNews(num_pages=10, year=y, query=q)
    asyncio.run(scraper.get_all_news())
    scraper.save_to_json(output_file)
    fin = time.time()

    print(f"TIME: {fin - inicio} seconds")
