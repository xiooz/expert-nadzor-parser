# -*- coding: utf-8-*-
import re
import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

LOGINURL = 'https://expert.nadzor-info.ru/login'
USERNAME = ''
PASSWORD = ''
URL = ''
SAVE_FILE = 'exp1.xls'

session = requests.Session()
CSRF = re.search(
    '(?<=csrftoken=)\w+',
    session.get(LOGINURL).headers['Set-Cookie']
)

req_headers = {
    'content-type': 'application/x-www-form-urlencoded',
    'accept': 'text/html, application/xhtml+xml',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ru-RU, ru;q=0.8,en-US;q=0.6,en;q=0.4',
    'cache-control': 'max-age=0',
    'host': 'expert.nadzor-info.ru',
    'upgrade-insecure-requests': '1'
}

form_data = {
    'username': USERNAME,
    'password': PASSWORD,
    'remember_me': 'on',
    'csrfmiddlewaretoken': CSRF.group(0)
}


def get_url(url, first_question, last_question, questions_count=0):
    # Authenticate
    r = session.post(LOGINURL, data=form_data, headers=req_headers, allow_redirects=True)

    wb = Workbook()
    ws = wb.active

    for i in range(first_question, last_question + 1):
        r2 = session.get('%s/%d/' % (url, i))
        # print('---------DATA-----------')
        print('#%d, %d' % (i - first_question + 1, i))
        print(r2.status_code)

        soup = BeautifulSoup(r2.text, 'html.parser')
        answer_list = soup.find_all('div', {'class': 'question'})

        for tag in answer_list:
            q_num = tag.find('h2', {'class': 'question__question'}).text
            question = tag.find('div', {'class': 'question__text'}).text
            answer = tag.find('div', {'class': 'answers__preparation-answer-text'})
            document = tag.find('div', {'class': 'answers__answer-ntd'})
            
            if isinstance(answer, type(None)):
                answer = ''
                print("no answer")
            else:
                answer = answer.text
            if isinstance(document, type(None)):
                document = ''
                print("no ntd")
            else:
                document = document.text

            ws.append([
                (re.search('\d+', q_num)).group(),
                question.strip(), answer.strip(), document.strip()
            ])
    wb.save(SAVE_FILE)


get_url(URL, 133927, 134152)
