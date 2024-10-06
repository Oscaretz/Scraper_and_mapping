import aiohttp, asyncio, json, os, time
from datetime import datetime
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

class GoogleSearchNews:
    def __init__(self, nqueries, query, qexception, qoption, qrangedate, qsite, ):
        self.nqueries = nqueries
        self.noticias = {}
        self.user_agent = UserAgent()
        self.query = query
        self.qoption = qoption
        self.qexception = qexception
        self.qrangedate = qrangedate
        self.qsite = qsite

    #Collecting the news information.
    async def get_info_new(self, session, url):
        async with session.get(url, headers={'User-Agent': self.user_agent.random}) as response:
            try:
                response.raise_for_status()
                text = await response.text()
                soup = BeautifulSoup(text, 'html.parser')
                news_elements = soup.select('a.WlydOe')

                for element in news_elements:

                    # Ommit the element if the title doesn't exist
                    try:
                        title = element.select_one('div.n0jPhd.ynAwRc.MBeuO.nDgy9d').text.strip()
                    except:
                        continue

                    # Check if the source element exists
                    source_element = element.select_one('div.MgUUmf.NUnG9d > span')
                    source = source_element.text.strip() if source_element else 'Unknown Source'

                    # Extract link
                    link = element['href'] if 'href' in element.attrs else element.parent['href']

                    # Check if the date element exists
                    date_element = element.select_one('div.OSrXXb.rbYSKb.LfVVr > span')
                    date = date_element.text.strip() if date_element else 'No Date'

                    # Store the extracted news info
                    self.noticias[title] = {'Source': source, 'Link': link, 'Date': date}

            except aiohttp.ClientResponseError as e:
                print(f"Failed to access the page. ClientResponseError: {e}")
            except Exception as e:
                print(f"An error occurred: {e}")

    #Running the scraper asynchronous
    async def get_all_news(self):
        tasks = []
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=2)) as session:
            for page_num in range(1, int(self.nqueries) + 1):
                url = f"https://www.google.com/search?q={self.query.replace(',','%20')}+{self.qoption.replace(',','+OR')}+-{self.qexception.replace(',','+-')}+site%3A{self.qsite}&lr=&sca_esv=2cdbf9d7674441ef&sxsrf=ACQVn09LTw8Oz-QMTiJFOR7cBmlbGmXFjw%3A1711408457466&source=lnt&tbs=cdr%3A1%2Ccd_min%3A{self.qrangedate.replace('-','%2F').replace('/','%2Ccd_max%3A')}%2Cctr%3AcountryMX&tbm=nws&sxsrf=ACQVn08n6MZ5dLUWMKiVtyFXkWoTHss1PA%3A1709841442399&ei=IhzqZaz_F6arur8Pxr-4iAU&ved=0ahUKEwismK_e9-KEAxWmle4BHcYfDlEQ4dUDCA4&uact=5&oq=&gs_lp=Egxnd3Mtd2l6LW5ld3MiC2ludW5kYWNpw7NuMggQABiABBixAzIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABEjKJFC8A1ioE3AAeACQAQCYAcUBoAGTEKoBBDEuMTa4AQPIAQD4AQGYAgagArIFwgIFECEYoAHCAgYQABgWGB6YAwCIBgGSBwMwLjagB7Mt&sclient=gws-wiz-news&start={page_num -10}"
                tasks.append(self.get_info_new(session, url))
                await asyncio.sleep(5)

            await asyncio.gather(*tasks)

    #Saving the results on a JSON file
    def save_to_json(self, output_file='links.json'):
        with open(f'archivos/{output_file}', 'w', encoding='utf-8') as json_file:
            json.dump(self.noticias, json_file, indent=4, ensure_ascii=False)
        return os.path.join('archivos', 'links.json') #Return the path of the file

    def save_to_json_test(self): #Only for testing
        current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_file= f'links[{current_datetime}].json'
        with open(f'{output_file}', 'w', encoding='utf-8') as json_file:
            json.dump(self.noticias, json_file, indent=4, ensure_ascii=False)
        print(f"File saved as: {output_file}")
        return output_file

async def main(nqueries, query, qexception, qoption, qrangedate, qsite):

    scraper = GoogleSearchNews(nqueries, query, qexception, qoption, qrangedate, qsite)
    await scraper.get_all_news()
    result = scraper.save_to_json()
    return result  
