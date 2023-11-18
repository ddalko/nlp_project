# step1.프로젝트에 필요한 패키지 불러오기
import argparse
import os
import  time
import  math
from pathlib import Path

from  selenium  import  webdriver
from  selenium.webdriver.common.keys  import  Keys
from  selenium.webdriver.common.by  import  By
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE
import selenium
import  pandas  as  pd

def get_args_parser():
    parser = argparse.ArgumentParser("JobPlanet web crawling script", add_help=False)
    parser.add_argument("--id", required=True, type=str)
    parser.add_argument("--pw", required=True, type=str)
    parser.add_argument("--start_page", required=True, type=int)
    parser.add_argument("--end_page", required=True, type=int)
    parser.add_argument("--output_dir", required=True, type=str)
    parser.add_argument("--maximum_review", required=True, type=str, help="최대 리뷰 개수 제한, 설정 값 보다 리뷰 수가 적다면 변함 없음.")
    return parser

# step3.크롬드라이버 실행 및 잡플래닛 로그인 함수
def  login(driver,  usr,  pwd):
    driver.get("https://www.jobplanet.co.kr/users/sign_in?_nav=gb")
    time.sleep(5)

    # 아이디 입력
    login_id  =  driver.find_element(By.ID,  "user_email")
    login_id.send_keys(usr)

    # 비밀번호 입력
    login_pwd  =  driver.find_element(By.ID,  "user_password")
    login_pwd.send_keys(pwd)

    # 로그인 버튼 클릭
    login_id.send_keys(Keys.RETURN)
    time.sleep(5)

# step4.원하는 회사의 리뷰 페이지까지 이동 함수
def  go_to_review_page(driver,  query):
    # 검색창에 회사명 입력
    search_query  =  driver.find_element(By.ID,  "search_bar_search_query")
    search_query.send_keys(query)
    search_query.send_keys(Keys.RETURN)
    time.sleep(3)

    # 회사명 클릭
    driver.find_element(By.CLASS_NAME,  "tit").click()
    time.sleep(5)

    # 팝업창 제거
    try:
        driver.find_element(By.CLASS_NAME,  "btn_close_x_ty1").click()
    except selenium.common.exceptions.ElementNotInteractableException as eniex:
        print(eniex)
    time.sleep(3)


# step5. 별점 변환 함수
def  parse_star_rating(style_attribute) -> float:
    if  len(style_attribute)  ==  11:
        rating_value  =  int(style_attribute[7:9])
        return  float(rating_value/20)
    else:
        return  5.0


# step6.데이터 크롤링 함수 (직무/근속여부/일시/요약/평점/장점/단점/경영진에게 바라는 점)
def  scrape_data(driver, maximum_review):
    list_div  =  []
    list_cur  =  []
    list_stars  =  []
    list_summery  =  []
    list_merit  =  []
    list_disadvantages  =  []
    list_opinions  =  []

    # 크롤링 할 리뷰 갯수 파악
    review_count  =  driver.find_element(By.ID,  "viewReviewsTitle")
    review_count  =  review_count.find_element(By.CLASS_NAME,  "num").text

    # 크롤링 할 페이지수 파악
    page  =  math.ceil(int(review_count.replace(',',''))/5)

    for  _  in  range(min(page, maximum_review)):
        review_box  =  driver.find_elements(By.CLASS_NAME,  "content_wrap")
        # 페이지당 최대 5개의 리뷰 박스 존재
        division = None
        current = None
        star = None
        summary = None
        merit = None
        disadvantage = None
        opinion = None
        for  i  in  review_box:
            user_info  =  i.find_elements(By.CLASS_NAME,  "txt1")
            # 직무
            try:
                division  =  user_info[0].text
            except:
                division = "직무 모름"
                
            # 재직여부
            try:
                current  =  user_info[1].text
            except:
                current = "재직 여부 모름"

            # 날짜
            # try:
            #     date  =  user_info[3].text
            # except:  #날짜 없는 경우 예외처리
            #     date  =  "날짜 없음"

            # 리뷰 요약
            try:
                summary  =  i.find_element(By.CLASS_NAME,  "us_label ").text
            except:  #신고로 인해 리뷰 요약 없는 경우 예외처리
                summary_ban  =  i.find_element(By.CLASS_NAME,  "cont_discontinu.discontinu_category")
                summary = summary_ban.text
                merit = summary_ban.text
                disadvantage = summary_ban.text
                opinion = summary_ban.text  

            # 장점, 단점, 경영진에게 바라는 점
            merit, disadvantage, opinion = None, None, None
            try:
                contents  =  i.find_elements(By.CLASS_NAME,  "df1")
                merit  =  contents[0].text
                disadvantage  =  contents[1].text
                opinion  =  contents[2].text
            except:
                merit = "장점 없음"
                disadvantage = "단점 없음"
                opinion = "경영진에게 바라는 점 없음"

            try:
                stars  =  i.find_elements(By.CLASS_NAME,  "star_score")
                for  _star  in  stars:
                    star = parse_star_rating(_star.get_attribute('style'))
            except:
                star = "별점 없음"
        print(division, star, current, summary, merit, disadvantage, opinion)
        if all([division, star, current, summary, merit, disadvantage, opinion]):
            list_div.append(ILLEGAL_CHARACTERS_RE.sub(r"", division))
            list_cur.append(ILLEGAL_CHARACTERS_RE.sub(r"", current))
            list_stars.append(star)
            list_summery.append(ILLEGAL_CHARACTERS_RE.sub(r"", summary))
            list_merit.append(ILLEGAL_CHARACTERS_RE.sub(r"", merit))
            list_disadvantages.append(ILLEGAL_CHARACTERS_RE.sub(r"", disadvantage))
            list_opinions.append(ILLEGAL_CHARACTERS_RE.sub(r"", opinion))

        try:
            driver.find_element(By.CLASS_NAME,  "btn_pgnext").click()
            time.sleep(5)
        except:
            pass

    total_data  =  pd.DataFrame({
        '직무':  list_div,
        '고용 현황':  list_cur,
        '별점':  list_stars,
        '요약':  list_summery,
        '장점':  list_merit,
        '단점':  list_disadvantages,
        '경영진에게 바라는 점':  list_opinions
    })

    return  total_data

def get_it_company_list(driver, start_page_idx: int, end_page_idx: int) -> list:
    it_company_list = []
    # nav start_page_idx ~ end_page_idx
    for page_idx in range(start_page_idx, end_page_idx+1):
        driver.get(f"https://www.jobplanet.co.kr/companies?sort_by=review_survey_total_avg_cache&industry_id=700&amp;page={page_idx}")
        # Get current page 회사명
        company_list = driver.find_elements(By.CLASS_NAME,  "us_titb_l3")
        for company in company_list:
            company_name = company.text.replace("following", "").strip()
            print(company_name)
            it_company_list.append(company_name)
        time.sleep(5)
    return it_company_list


def  main(args):
    # 크롬 드라이버 실행
    driver = webdriver.Chrome()
    # 로그인
    login(driver,  args.id,  args.pw)
    # 기업 목록 조회
    it_company_list = get_it_company_list(driver, args.start_page, args.end_page)

    for query in it_company_list:
        try:
            # 리뷰 페이지로 이동
            go_to_review_page(driver,  query)
            # 리뷰 클롤링
            total_data  =  scrape_data(driver, args.maximum_review)
            # 엑셀 파일로 저장
            excel_path = os.path.join(args.output_dir, f"review_{query}.xlsx")
            total_data.to_excel(excel_path, index=True)
        except selenium.common.exceptions.NoSuchElementException as nseex:
            print(nseex)
        except selenium.common.exceptions.InvalidSessionIdException as isie:
            print(isie)

    # 크롬 드라이버 종료
    driver.close()


if  __name__  ==  "__main__":
    parser = argparse.ArgumentParser(
        "JobPlanet web crawling script", parents=[get_args_parser()]
    )
    args = parser.parse_args()
    if args.output_dir:
        Path(args.output_dir).mkdir(parents=True, exist_ok=True)
    main(args)
