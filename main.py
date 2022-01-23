import requests
import bs4

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) '
                         'Gecko/20100101 Firefox/96.0',
           'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
           'Sec-Fetch-Dest': 'document',
           'Sec-Fetch-Mode': 'navigate',
           'Sec-Fetch-Site': 'cross-site',
           'Connection': 'keep-alive',
           'Cookie': 'hl=ru; fl=ru; feature_streaming_comments=true; '
                     'visited_articles=63539:281861:101678:539968; '
                     'habr_web_home=ARTICLES_LIST_ALL',
           'If-None-Match': 'W/"361d1-IeEJm0Ue3E0v6R4PhpnECEEoHtg"',
           'Cache-Control': 'max-age=0'
           }

keywords = ['дизайн', 'фото', 'web', 'python']


def get_request(link):
    res = requests.get(link, headers=headers)
    res.raise_for_status()
    text = res.text
    soup = bs4.BeautifulSoup(text, features='html.parser')
    return soup


def habr_scraping():
    link = 'https://habr.com/ru/all/'
    req = get_request(link)
    articles = req.find_all('article')

    for article in articles:
        href = article.find('h2').find('a')['href']
        article_link = f'https://habr.com{href}'
        article = get_request(article_link)
        article_text = article.find('div', id='post-content-body').text.lower()
        if set(keywords) & set(article_text.split()):
            title = article.find('h1').text
            date = article.find(
                'span', class_='tm-article-snippet__datetime-published'
            ).find('time')['title']
            print(f'{date} | {title} | {article_link}')


if __name__ == '__main__':
    habr_scraping()
