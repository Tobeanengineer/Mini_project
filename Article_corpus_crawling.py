# KBS World Radio으로부터 다국어 raw corpus 수집 및 저장 프로그램

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import re

# 크롬창이 안보이도록 설정
options = Options()
options.headless = True
options.add_argument('--window-size=1920x1080')
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(10)

print(''' 
### 다국어 코퍼스 크롤러 ###

1. 한국어
2. 아랍어
3. 중국어
4. 프랑스어
5. 독일어
6. 인도네시아어
7. 일본어
8. 러시아어
9. 스페인어
10. 베트남어
11. 영어
프로그램을 종료하려면 숫자 1번을 눌러주세요.

### 언어명으로 입력해 주세요. ###
''')

language = {
    '한국어' : 'k',
    '아랍어' : 'a',
    '중국어' : 'c',
    '프랑스어' : 'f',
    '독일어' : 'g',
    '인도네시아어' : 'i',
    '일본어' : 'j',
    '러시아어' : 'r',
    '스페인어' : 's',
    '베트남어' : 'v',
    '영어' : 'e'
}


class crawler:
    pattern = re.compile('[\{\}\[\]\/?,;:|\)*~`!^+<>@\#$&\\\=\(\'\"…·]')
    url = 'http://world.kbs.co.kr/service/news_list.htm?page={}&lang={}&id='


    def __init__(self, num, lang):
        self.article_title, self.article_list = [], []
        self.article_index, self.page = 1, 1
        self.article_count = 0
        self.article_num = num
        self.language = lang

    def title_crawl(self) -> dict:
        while True:
            if self.article_count == self.article_num+1:
                break

            else:
                driver.get(self.url.format(self.page, self.language))

                try:
                    title = driver.find_element_by_xpath(
                        f'// *[ @ id = "container"] / div / section[2] / article[{self.article_index}] / h2 / a')
                    self.article_title.append(title.text)

                    article_page = driver.find_element_by_xpath(f'//*[@id="container"]/div/section[2]/article[{self.article_index}]/h2/a')
                    article_page.click()

                except:
                    # 클릭 대상이 쿠키 수집창일 경우
                    close_ad = driver.find_element_by_xpath('//*[@id="wrap"]/div[2]/div/a')
                    close_ad.click()

                    title = driver.find_element_by_xpath(
                        f'// *[ @ id = "container"] / div / section[2] / article[{self.article_index}] / h2 / a')
                    self.article_title.append(title.text)

                    article_page = driver.find_element_by_xpath(
                        f'//*[@id="container"]/div/section[2]/article[{self.article_index}]/h2/a')
                    article_page.click()

                # 'Photo :' 등 사진 쓸모없는 텍스트 제거 작업
                raw_text = driver.find_element_by_xpath('//*[@id="ele1"]/div[3]')
                raw_text = str(raw_text.text).strip()

                raw_text_list = raw_text.split('\n') # 쓸모없는 텍스트는 공백으로 구분, 제거하여 [1]만 집어넣어줌
                article = ' '.join(raw_text_list[1:])

                self.article_list.append(article)
                self.article_count += 1
                driver.back()

                # 기사가 한 페이지에 10개 씩 들어가므로, 페이지의 마지막 기사까지 클릭하면 페이지는 늘리고 기사 인덱스 초기화
                if self.article_index == 10:
                    self.page += 1
                    self.article_index = 1

                self.article_index += 1


        driver.quit()

        # 기사 제목과 내용에 대해서 특수문자와 쓸모없는 이중공백 제거
        self.article_title = [re.sub(self.pattern, ' ', title) for title in self.article_title]
        self.article_title = [title.replace('  ', ' ') for title in self.article_title]

        self.article_list = [re.sub(self.pattern, '', article).strip() for article in self.article_list]
        self.article_list = [article.replace('  ', ' ') for article in self.article_list]

        dic_article = dict(zip(self.article_title, self.article_list))
        return dic_article

    # csv 변환 파일
    def data_to_csv(self, dic_file: dict) -> 'csv':
        # 현재 경로에 csv 파일 저장
        df = pd.DataFrame.from_dict(dic_file, orient='index', columns=['article'])
        df.to_csv(f'./{lang_input}_corpus_file.csv', encoding='utf-8-sig')

        # 차후 사용할 일이 있을 수 있으므로 데이터프레임 자체는 변수에 할당해줌
        return df


if __name__ == '__main__':
    try:
        lang_input = input('찾을 언어를 입력해 주세요 : ')
        select_lang = language[lang_input]
        article_num = int(input('가져올 기사의 개수 : '))
        print(f'{lang_input} 기사 코퍼스를 수집 중입니다. 데이터의 양에 따라 시간이 다소 걸릴 수 있습니다.')


    except KeyError:
        print('잘못된 입력입니다. 다시 입력해 주세요.')

    data_crawl = crawler(article_num, select_lang).title_crawl()
    data_csv = crawler(article_num, select_lang).data_to_csv(data_crawl)

    print('크롤링 완료!')

