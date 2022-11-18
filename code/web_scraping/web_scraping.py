"""[web scraping モジュール]
web scrapingクラス定義
"""
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
import time


class WebScraping(webdriver.Chrome):
    """WebScrapingクラス

    Args:
        webdriver (_type_): _description_
    """
    def __init__(self,
                 url="https://www.google.com/",
                 executable_path=ChromeDriverManager().install(),
                 port=0, options=None,
                 service_args=None,
                 desired_capabilities=None,
                 service_log_path=None,
                 chrome_options=None,
                 keep_alive=True):
        """初期化

        Args:
            (url (str, optional):
             _description_. Defaults to "https://www.google.com/".)
            (executable_path (_type_, optional):
             _description_. Defaults to ChromeDriverManager().install().)
            port (int, optional): _description_. Defaults to 0.
            options (_type_, optional): _description_. Defaults to None.
            service_args (_type_, optional): _description_. Defaults to None.
            (desired_capabilities (_type_, optional):
             _description_. Defaults to None.)
            (service_log_path (_type_, optional):
             _description_. Defaults to None.)
            chrome_options (_type_, optional): _description_. Defaults to None.
            keep_alive (bool, optional): _description_. Defaults to True.
        """
        super().__init__(executable_path, port, options,
                         service_args, desired_capabilities,
                         service_log_path,
                         chrome_options, keep_alive)
        self.maximize_window()
        self.get(url)

    def read_page(self):
        """ページ情報の取得
        """
        try:
            html = self.page_source.encode('utf-8')
            soup = bs(html, "html.parser")
        except Exception:
            print('error')
        else:
            self.soup = soup

    def input_google_serch(self, keyword: str):
        """Google検索入力

        Args:
            keyword (str): キーワード
        """
        from selenium.webdriver.common.keys import Keys
        self.get("https://google.com/")
        time.sleep(2)
        browser_from = self.find_element_by_class_name('gLFyf.gsfi')
        browser_from.send_keys(keyword)
        browser_from.send_keys(Keys.ENTER)

    def get_google_list(self, page_count: int) -> list:
        """Google検索のリストを取得するメソッド

        Args:
            page_count (int): ページ数

        Returns:
            list: _description_
        """
        site_list = []
        for page in range(page_count):
            self.read_page()
            contents = (self.soup.find('div', {'id': 'center_col'})
                        .find('div', {'id': 'rso'}))
            for content in contents:
                try:
                    con1 = content.find('div', {'class': 'yuRUbf'})
                    script = content.find('div', {'class': 'Z26q7c UK95Uc'})
                    c_u = con1.find('a').get('href')
                    google_title = con1.find('h3').text
                    script = script.text
                except Exception:
                    pass
                    script = 'No data'
                else:
                    site_list.append({
                        'title': google_title,
                        'url': c_u,
                        'discription': script
                        })
            try:
                browser_from = self.find_element_by_id('pnnext')
            except Exception as ex:
                print(ex)
                break
            else:
                browser_from.click()
                time.sleep(2)
        return site_list

    def collect_google_map_list(self, page_count: int = 10) -> list:
        """_summary_

        Args:
            page_count (int, optional): _description_. Defaults to 10.

        Returns:
            list: _description_
        """
        item_list = []
        count = len(item_list)
        for _ in range(page_count):
            self.read_page()
            items = self.soup.find_all('div', {'jsname': 'GZq3Ke'})
            select_ids = []
            for ids in items:
                select_ids.append(ids.get('id'))
            for i, select_id in enumerate(select_ids):
                elem = self.find_element_by_id(select_id)
                elem.click()
                time.sleep(2)
                self.read_page()
                a = self.soup
                soup_page = a.find('div', {'class': 'ifM9O'})
                try:
                    shop_name = (soup_page.find('h2', {'data-attrid': 'title'})
                                 .find('span').text)
                except Exception:
                    print('pass')
                    continue
                else:
                    try:
                        source = (soup_page
                                  .find('div', {'class': 'IzNS7c duf-h'})
                                  .find('div', {'class': 'QqG1Sd'}))
                        if source.text == 'ウェブサイト':
                            shop_url = source.find('a').get('href')
                        else:
                            shop_url = 'No data'
                    except Exception:
                        pass
                    else:
                        shop_url = 'No data'

                    try:
                        genre = (soup_page
                                 .find('div', {'class': 'zloOqf kpS1Ac vk_gy'})
                                 .text)
                        service = (soup_page
                                   .find('div', {'class': 'wDYxhc NFQFxe'})
                                   .text
                                   .replace('\xa0', ' ')
                                   .replace('サービス オプション:', ''))
                    except Exception:
                        genre = 'No data'
                        service = 'No data'
                    try:
                        tell = a.find('span', {'class':
                                               'LrzXr zdqRlf kno-fv'}).text
                    except Exception:
                        tell = 'No data'
                    try:
                        source_2 = soup_page.find('div', {'class':
                                                          'TLYLSe'})
                        star = source_2.find('span', {'class':
                                                      'Aq14fc'}).text
                    except Exception:
                        star = 'No data'
                        coment_count = 'No data'
                    else:
                        coment_count = (source_2.find('a').text
                                        .replace('Google のクチコミ（', '')
                                        .replace('）', ''))
                    try:
                        post_address = (a.find('div', {'class': 'BOu6vf'})
                                        .text.split())
                        post = post_address[0]
                        address = post_address[1:]
                    except Exception:
                        post = 'No data'
                        address = 'No data'

                    item_list.append({
                        'shop_name': shop_name,
                        'genre': genre,
                        'service': service,
                        'post': post,
                        'address': address,
                        'tell': tell,
                        'shop_url': shop_url,
                        'star': star,
                        'coment_count': coment_count
                    })
                    print(f'{count}: {i} : {shop_name}-OK')
                    count += 1

            next_url = self.soup.find('a', {'id': 'pnnext'})

            try:
                url = 'https://www.google.com/{}'.format(next_url.get('href'))
            except Exception:
                break
            else:
                self.get(url)
                time.sleep(2)

        print(len(item_list))
        return item_list


class WebScraping_head_less(WebScraping):
    options = Options()
    options.add_argument('--headless')

    def __init__(self,
                 url="https://www.google.com/",
                 executable_path=ChromeDriverManager().install(),
                 port=0,
                 options=options,
                 service_args=None,
                 desired_capabilities=None,
                 service_log_path=None,
                 chrome_options=None,
                 keep_alive=True):
        super().__init__(url,
                         executable_path,
                         port,
                         options,
                         service_args,
                         desired_capabilities,
                         service_log_path,
                         chrome_options,
                         keep_alive)
