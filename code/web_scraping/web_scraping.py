"""[web scraping モジュール]
web scrapingクラス定義
"""
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs


def start_browser(url='https://www.google.com/', head_less=False):
    """[セレニウムブラウザー起動]
    Args:
        url (str, optional): [URL]. Defaults to 'https://www.google.com/'.
    Returns:
        [Selenium.Webdriver]: [インスタンス]
    """
    if head_less:
        options = Options()
        options.add_argument('--headless')
        browser = (webdriver.Chrome(ChromeDriverManager().install(),
                   chrome_options=options))
    else:
        browser = webdriver.Chrome(ChromeDriverManager().install())
        browser.maximize_window()
    browser.get(url)
    return browser


class WebScraping():
    """WebScrapingクラス

　　Attributes:
　　　head_less(bool): ヘッドレスモードの設定
    """

    def __init__(self, head_less=False):
        """初期化

        Args:
            head_less (bool, optional): ヘッドレスモードの設定. Defaults to False.
        """
        self.browser = start_browser(head_less=head_less)

    def read_page(self):
        """ページ情報の取得
        """
        try:
            html = self.browser.page_source.encode('utf-8')
            soup = bs(html, "html.parser")
        except Exception:
            print('error')
        else:
            self.soup = soup
