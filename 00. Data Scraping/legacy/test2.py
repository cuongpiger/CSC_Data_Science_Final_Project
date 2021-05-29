from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


url1 = "https://shopee.vn/-M%C3%A3-FAMAYMA2-gi%E1%BA%A3m-10K-%C4%91%C6%A1n-50K-%C3%81o-thun-nam-n%E1%BB%AF-form-r%E1%BB%99ng-Yinxx-%C3%A1o-ph%C3%B4ng-tay-l%E1%BB%A1-ATL43-i.14746382.6519318270"
url2 = "https://shopee.vn/%C3%81o-Len-C%E1%BB%95-3p-Body-N%E1%BB%AF-FREESHIP-%F0%9F%8C%B8-%C3%81o-thun-t%C4%83m-d%C3%A1ng-%C3%B4m-d%C3%A0i-tay-nhi%E1%BB%81u-m%C3%A0u-ki%E1%BB%83u-d%C3%A1ng-basic-Ulzzang-QC-SI%C3%8AU-HOT-%F0%9F%8C%B8-i.98758274.7003495622"
url3 = "https://shopee.vn/-Bigsize-38-46-n%C3%A2ng-ng%E1%BB%B1c-ch%E1%BB%91ng-ch%E1%BA%A3y-x%E1%BB%87-%C3%81o-l%C3%B3t-bigsize-%C3%A1o-ng%E1%BB%B1c-bigsize-Th%C3%A1i-Lan-AN343-i.907018.1021926140"


class Review:
    def __init__(self, pComment, pRating):
        self.iComment = pComment
        self.iRating = pRating


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
    


def getAllRevirewsOfProduct(pUrl):
    stop = False
    driver = webdriver.Firefox()
    locator_button_focus = (By.CLASS_NAME, "shopee-button-solid--primary")
    locator_button = (By.CLASS_NAME, "shopee-icon-button--right")
    buttons_box = {}
    customers_reviews = []

    while True:
        flag = None
        try:
            driver.get(pUrl)
            wait = WebDriverWait(driver, 20)

            scroll(driver, wait)
            flag = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.shopee-product-rating")))
            
        except TimeoutException as e:
            continue
        finally:
            while True:
                if flag is not None:
                    reviews = driver.find_elements_by_css_selector("div.shopee-product-rating")
                    for review in reviews:
                        comment = review.find_element_by_class_name("shopee-product-rating__content").text
                        rating = len(review.find_elements_by_class_name("icon-rating-solid--active"))
                        print(f"{rating} - {comment}")
                        
                        new_review = Review(comment, rating)
                        customers_reviews.append(new_review)
                    
                    flag1 = None
                    while True:
                        flag1 = None
                        try:
                            flag1 = wait.until(EC.element_to_be_clickable(locator_button))
                            
                            if flag1 is not None:
                                flag1.click()
                        except TimeoutException as e:
                            continue
                        finally:
                            break
                        
                    while flag1 is not None:
                        flag2 = None
                        try:
                            flag2 = wait.until(EC.presence_of_element_located(locator_button_focus))
                            
                            if flag2 is not None:
                                key = flag2.text.strip()
                                buttons_box[key] = buttons_box.get(key, 0) + 1
                                
                                if buttons_box.get(key) > 1:
                                    driver.close()
                                    driver.quit()
                                    stop = True
                                    break
                                
                        except TimeoutException as e:
                            continue
                        finally:
                            break
                        
                if stop: break
                
                flag = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.shopee-product-rating")))
                
            return customers_reviews
                
reviews = getAllRevirewsOfProduct(url3)

for review in reviews[:5]:
    print(f"{review.iRating} - {review.iComment}")