import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re

import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

def crawl_data(url, name, filename='이재호.csv'):
    page_num = 1  # 페이지 번호 초기화

    while True:
        try:
            page_url = url + f'&page={page_num}'
            html = urlopen(page_url)
            bs = BeautifulSoup(html, 'html.parser')

            q_tbody = bs.find('tbody').find_all('tr')

            # 필드 추출
            fields = [q.find('td', class_='field').text for q in q_tbody]

            # 링크 추출
            links = [q.find('a').get('href') for q in q_tbody]

            # 제목 추출
            titles = [q.find('a').text for q in q_tbody]

            # 질문 추출
            questions = []
            # 링크 안에 들어가서 질문 추출
            for link in links:
                try:
                    html = urlopen('https://kin.naver.com/'+link)
                    bs = BeautifulSoup(html, 'html.parser')
                    question = bs.find('div', class_='questionDetail').text
                    cleaned_question = re.sub(r'[\n\t\r\xa0]', '', question)
                    questions.append(cleaned_question)
                except Exception as e:
                    print("Error occurred while fetching question:", e)
                    questions.append("nan")  # 에러가 발생하면 'nan'을 추가

            # 링크 안에 들어가서 답변 추출
            answers = []  # 페이지의 모든 답변을 담을 리스트
            for link in links:
                try:
                    html = urlopen('https://kin.naver.com/'+link)
                    bs = BeautifulSoup(html, 'html.parser')
                    # 답변 작성자 확인
                    author = bs.find('strong', class_='name').text.strip()
                    # 답변 작성자가 이재호인 경우에만 답변 추출
                    if author == name:
                        answer_elements = bs.find_all('p', class_='se-text-paragraph')
                        if not answer_elements:
                            answers.append("nan")  # 답변이 없는 경우 'nan'을 추가
                        else:
                            # 각 답변을 문자열로 변환하여 합침
                            combined_answer = " ".join([element.text.strip() for element in answer_elements])
                            answers.append(combined_answer)  # 답변을 리스트에 추가
                except Exception as e:
                    print("Error occurred while fetching answers for link:", link, e)
                    answers.append("nan")  # 에러가 발생하면 'nan'을 추가

            # 최종 questions ( 제목 + 질문 )
            questions = [title + ' ' + question for title, question in zip(titles, questions)]

            # 데이터프레임 생성
            df = pd.DataFrame({'field': fields, 'question': questions, 'answer': answers})
            file_path = './data/' + filename
            df.to_csv(file_path, mode='a', header=False, index=False)

            print(f"Page {page_num} crawled successfully.")

            page_num += 1  # 다음 페이지로 이동

        except Exception as e:
            print("Error occurred while crawling page", page_num, ":", e)
            break  # 페이지를 더 이상 크롤링할 수 없는 경우 반복문 종료

# url_lee = 'https://kin.naver.com/userinfo/expert/answerList.naver?u=dEgr29uBZ5z0sTY%2FIic1U8r4rT%2BfX97EC6sMbz2os5Q%3D'
# crawl_data(url_lee, '이재호')

url_you = 'https://kin.naver.com/userinfo/expert/answerList.naver?u=vWlXGDBdOqyyM9ZZj5apMuUJWtcX5NndIARjqyYdUY0%3D'
crawl_data(url_you, '유성권')
