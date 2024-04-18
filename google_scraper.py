import aiohttp, asyncio, json, os
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


class GoogleSearchNews:
    def __init__(self, num_pages, query, qexception, qoption, qrangedate, qsite):
        self.num_pages = num_pages
        self.noticias = {}
        self.user_agent = UserAgent()
        self.query = query
        self.qoption = qoption
        self.qexception = qexception
        self.qrangedate = qrangedate
        self.qsite = qsite

    async def get_info_new(self, session, url):
        async with session.get(url, headers={'User-Agent': self.user_agent.random}) as response:
            try:
                response.raise_for_status()
                text = await response.text()
                print("Response text:", text)  # Debugging
                soup = BeautifulSoup(await response.text(), 'html.parser')
                news_elements = soup.select('a.WlydOe')

                for element in news_elements:
                    source = element.select_one('div.MgUUmf.NUnG9d > span').text.strip()
                    title = element.select_one('div.n0jPhd.ynAwRc.MBeuO.nDgy9d').text.strip()
                    link = element['href'] if 'href' in element.attrs else element.parent['href']
                    date = element.select_one('div.OSrXXb.rbYSKb.LfVVr > span').text.strip()

                    self.noticias[title] = {'Source': source, 'Link': link, 'Date': date}

            except aiohttp.ClientResponseError as e:
                print(f"Failed to access the page. ClientResponseError: {e}")

    async def get_all_news(self):
        tasks = []
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=10)) as session:
            for page_num in range(1, self.num_pages + 1):
                url = f"https://www.google.com/search?q={self.query.replace(',','%20')}+{self.qoption.replace(',','+OR')}+-{self.qexception.replace(',','+-')}+site%3A{self.qsite}&lr=&sca_esv=2cdbf9d7674441ef&sxsrf=ACQVn09LTw8Oz-QMTiJFOR7cBmlbGmXFjw%3A1711408457466&source=lnt&tbs=cdr%3A1%2Ccd_min%3A{self.qrangedate.replace('-','%2F').replace('/','%2Ccd_max%3A')}%2Cctr%3AcountryMX&tbm=nws&sxsrf=ACQVn08n6MZ5dLUWMKiVtyFXkWoTHss1PA%3A1709841442399&ei=IhzqZaz_F6arur8Pxr-4iAU&ved=0ahUKEwismK_e9-KEAxWmle4BHcYfDlEQ4dUDCA4&uact=5&oq=&gs_lp=Egxnd3Mtd2l6LW5ld3MiC2ludW5kYWNpw7NuMggQABiABBixAzIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABEjKJFC8A1ioE3AAeACQAQCYAcUBoAGTEKoBBDEuMTa4AQPIAQD4AQGYAgagArIFwgIFECEYoAHCAgYQABgWGB6YAwCIBgGSBwMwLjagB7Mt&sclient=gws-wiz-news&start={page_num*10 -10}"
                tasks.append(self.get_info_new(session, url))

            await asyncio.gather(*tasks)

    def save_to_json(self, output_file='links.json'):
        with open(f'archivos/{output_file}', 'w', encoding='utf-8') as json_file:
            json.dump(self.noticias, json_file, indent=4, ensure_ascii=False)
        return os.path.join('archivos', 'links.json')

async def main(num_pages, query, qexception, qoption, qrangedate, qsite):

    scraper = GoogleSearchNews(num_pages, query, qexception, qoption, qrangedate, qsite)
    await scraper.get_all_news()
    result = scraper.save_to_json()
    return result



