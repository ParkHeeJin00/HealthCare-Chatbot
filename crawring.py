import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError
import re
import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError
import re

# 크롤링 함수
def crawl_data(url, name):
    page_num = 1  # 크롤링할 페이지 번호
    # page_num이 1인 경우에 컬럼만 적힌 csv 파일을 생성
    if page_num == 1:
        df = pd.DataFrame(columns=['field', 'question', 'answer'])
        file_path = './data/' + name + '.csv'
        df.to_csv(file_path, mode='w', index=False)

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

            # 답변 추출
            answers = []

            # 링크 안에 들어가서 질문과 답변 추출
            for link in links:
                try: 
                    html = urlopen('https://kin.naver.com/'+link)
                    bs = BeautifulSoup(html, 'html.parser')
                    question_elements = bs.find('div', class_='questionDetail')
                    question = question_elements.text.strip()
                    cleaned_question = re.sub(r'[\n\t\r\xa0]', '', question)
                    questions.append(cleaned_question)

                    answer_elements = bs.find_all('div', id=re.compile('^answer_\d+$'))
                    for answer_element in answer_elements:      
                        author = answer_element.find('strong', class_='name').text.strip()
                        if author == name:
                            answer = answer_element.find_all('p', class_='se-text-paragraph')
                            answer_texts = [p.text.strip().replace('\u200b', '') for p in answer]
                            combined_answer = " ".join(answer_texts)
                            answers.append(combined_answer)
                except Exception as e:
                    print("Error questions for link:", link, e)
                    questions.append(None)  # 에러가 발생한 경우 None 추가
                    answers.append(None)

            # 최종 questions ( 제목 + 질문 )
            questions = [title + ' ' + question if question else '' for title, question in zip(titles, questions)]

            # 데이터프레임 생성
            df = pd.DataFrame({'field': fields, 'question': questions, 'answer': answers})
            file_path = './data/' + name + '.csv'
            df.to_csv(file_path, mode='a', header=False, index=False)

            print(f"Page {page_num} crawled successfully.")

            page_num += 1  # 다음 페이지로 이동

        except HTTPError as e:
            if e.code == 403:
                print("링크가 비공개 처리되어 접근할 수 없습니다. 페이지를 스킵합니다.")
                page_num += 1  # 다음 페이지로 이동
                continue
            else:
                print("Error occurred while crawling page", page_num, ":", e)
                page_num += 1  # 다음 페이지로 이동

        except Exception as e:
            print("Error occurred while crawling page", page_num, ":", e)
            page_num += 1  # 페이지를 더 이상 크롤링할 수 없는 경우 반복문 종료





# 이재호 - 128,275개
# url_lee = 'https://kin.naver.com/userinfo/expert/answerList.naver?u=dEgr29uBZ5z0sTY%2FIic1U8r4rT%2BfX97EC6sMbz2os5Q%3D'
# crawl_data(url_lee, '이재호')

# 유성권 - 11,246개 - 완료
# url_you = 'https://kin.naver.com/userinfo/expert/answerList.naver?u=vWlXGDBdOqyyM9ZZj5apMuUJWtcX5NndIARjqyYdUY0%3D'
# crawl_data(url_you, '유성권')

# # 임동호 - 1,098개  - 완료
# url_em = 'https://kin.naver.com/userinfo/expert/answerList.naver?u=7Jx5T%2Bbm8dqisquYQuy361I5y5A7ANLCkiBHEa%2B0MRk%3D'
# crawl_data(url_em, '임동호')

# # 법무법인 리더스 - 17,486개
# url_reders = 'https://kin.naver.com/userinfo/answerList.naver?u=gmqETRj8%2FzezDhBH0ZMELbjaVB1IMfSeTqFsGSYCmUA%3D'
# crawl_data(url_reders, '법무법인 리더스')

# # 권진원 - 1,592개 - 완료
# url_gwon = 'https://kin.naver.com/userinfo/expert/answerList.naver?u=VAvw4Ith8rPTwkefEBW4H50zpG22e1OwKLeB15NoElc%3D'
# crawl_data(url_gwon, '권진원')

# # # 오지영 - 535개 - 완료
# url_oh = 'https://kin.naver.com/userinfo/expert/answerList.naver?u=vRM2dyNcboGc7Crw5A93l6K8XFIx%2FrvaK9jTngtd4kU%3D'
# crawl_data(url_oh, '오지영')

# # # 김정묵 - 3,089개
# url_kim = 'https://kin.naver.com/userinfo/expert/answerList.naver?u=FHm0d333w%2FK7aKXitxnMkkWPwgLXffNof3uNJZLAEYs%3D'
# crawl_data(url_kim, '김정묵')

# # # # 임동규 - 3,622개
# url_im = 'https://kin.naver.com/userinfo/expert/answerList.naver?u=blzE%2BEENitBXNBDxywmXb49gML4hyjHzs3I9zZIOhgo%3D'
# crawl_data(url_im, '임동규')

# # # # 장은영 - 2,155개 - 해야함
# url_jang = 'https://kin.naver.com/userinfo/expert/answerList.naver?u=M%2FklyESaBLWXyXapE%2BQvIFlyDbtrtzts8nKYgS5d0Hk%3D'
# crawl_data(url_jang, '장은영')

# # # 윤세라 - 1,040개 - 해야함
# url_yun = 'https://kin.naver.com/userinfo/expert/answerList.naver?u=adFOcJxekaTvqTczq6mIJvcOoiB6tMJ9nRXj2OkeYpA%3D'
# crawl_data(url_yun, '윤세라')