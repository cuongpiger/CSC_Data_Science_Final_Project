from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox()


def scroll(pDriver, pWait):
    last_height = pDriver.execute_script("return document.body.scrollHeight")
    pDriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    new_height = pDriver.execute_script("return document.body.scrollHeight")

    while new_height != last_height:
        pWait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.shopee-product-rating")))
        last_height = new_height
        pDriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        new_height = pDriver.execute_script("return document.body.scrollHeight")

    pDriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    


url1 = "https://shopee.vn/-M%C3%A3-FAMAYMA2-gi%E1%BA%A3m-10K-%C4%91%C6%A1n-50K-%C3%81o-thun-nam-n%E1%BB%AF-form-r%E1%BB%99ng-Yinxx-%C3%A1o-ph%C3%B4ng-tay-l%E1%BB%A1-ATL43-i.14746382.6519318270"
url2 = "https://shopee.vn/%C3%81o-Len-C%E1%BB%95-3p-Body-N%E1%BB%AF-FREESHIP-%F0%9F%8C%B8-%C3%81o-thun-t%C4%83m-d%C3%A1ng-%C3%B4m-d%C3%A0i-tay-nhi%E1%BB%81u-m%C3%A0u-ki%E1%BB%83u-d%C3%A1ng-basic-Ulzzang-QC-SI%C3%8AU-HOT-%F0%9F%8C%B8-i.98758274.7003495622"

while True:
    flag = None
    try:
        driver.get(url1)
        wait = WebDriverWait(driver, 20)

        scroll(driver, wait)
        flag = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.shopee-product-rating")))
        
    except TimeoutException as e:
        continue
    finally:
        if flag is not None:
            reviews = driver.find_elements_by_css_selector("div.shopee-product-rating")
            for review in reviews:
                comment = review.find_element_by_class_name("shopee-product-rating__content").text
                rating = len(review.find_elements_by_class_name("icon-rating-solid--active"))
                print(f"{rating} - {comment}")
            
            break

driver.quit()

"""
Code này chạy ổn, đừng chỉnh sửa gì hết, trả về comment của toàn bộ khách hàng ở pagination đầu tiên
"""