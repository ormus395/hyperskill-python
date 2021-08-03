import os
import string
import requests
from bs4 import BeautifulSoup

# ?searchType=journalSearch&sort=PubDate&page=2

def main():
    num_pages = int(input())
    article_type = input()
    page_count = 1
    url = ""

    while page_count <= num_pages:
        if page_count == 1:
            url = "https://www.nature.com/nature/articles"
        else:
            url = \
                f"https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&page={page_count}"

        r = requests.get(url)

        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')

            articles = soup.find_all('article')

            os.mkdir(f"Page_{page_count}")
            # scrape the page for the article type
            for article in articles:
                type = article.select_one('[data-test="article.type"]')

                if type:
                    type = type.text.strip()

                    if type == article_type:
                        print("article type found: " + type)
                        title = article.select_one('h3.c-card__title').text.lower().replace(' ', '_').replace(string.punctuation, '').strip()
                        article_link = article.select_one('a').get('href')
                        print("Article link: " + article_link)
                        article_request = requests.get("https://www.nature.com" + article_link)

                        if article_request.status_code == 200:
                            print("Fetched the articles content")
                            article_content = BeautifulSoup(article_request.content, 'html.parser')
                            article_body = article_content.find('div', attrs={'class':'article-item__body'})

                            if article_body:
                                print(os.getcwd())
                                file_name = title + '.txt'
                                file_path = os.getcwd() + '\\' + f"Page_{page_count}"
                                save_path = os.path.join(file_path, file_name)

                                article_binary = bytes(article_body.text.strip(), 'utf-8')
                                print(title)
                                file = open(save_path, 'wb')
                                # file = open(title + '.txt', 'wb')
                                file.write(article_binary)
                                file.close()
                                print('Finished writing to file')
                            else:
                                article_body = article_content.find('div', attrs={'class':'c-article-body'})
                                if article_body:
                                    print(os.getcwd())
                                    file_name = title + '.txt'
                                    file_path = os.getcwd() + '\\' + f"Page_{page_count}"
                                    save_path = os.path.join(file_path, file_name)

                                    article_binary = bytes(article_body.text.strip(), 'utf-8')
                                    print(title)
                                    file = open(save_path, 'wb')
                                    # file = open(title + '.txt', 'wb')
                                    file.write(article_binary)
                                    file.close()
                                    print('Finished writing to file')
                        else:
                            print('There was an issue navigating to the news article')
                # else:
                    # print('No news article was found')
        page_count += 1


main()


