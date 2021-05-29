from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
    

def goToFooterTag(pDriver):
    last_height = pDriver.execute_script("return document.body.scrollHeight") # chiều cao ban đầu của trang
    
    while True:
        try:
            pDriver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # lặn chuột xuống cuối trang
            WebDriverWait(pDriver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "footer"))) # chờ AJAX gửi data về trong tối đa 10 giây và chờ thẻ `footer` xuất hiện
            new_height = pDriver.execute_script("return document.body.scrollHeight") # lấy chiều cao hiện tại của trang
            
            if new_height != last_height: continue # thẻ `footer` chưa xuất hiện
        finally:
            return

def loadProductsURL(pUrlPattern: str, pRange, pProductPattern):
    driver = webdriver.Firefox()
    products_url = []
    
    for i in range(pRange[0], pRange[1]):
        url = f"{pUrlPattern}{i}"
        driver.get(url)
        goToFooterTag(driver)
    
        urls = [a_tag.get_attribute('href') for a_tag in driver.find_elements_by_css_selector(pProductPattern)]# lấy các địa chỉ URL đến sản phẩm
        products_url += urls
    
    driver.close()
    driver.quit()
    
    return products_url
    
def saveProductsURL(pPath, pListURLs):
    try:
        with open(pPath, 'w') as writer:
            writer.write("\n".join(pListURLs))
    except:
        print("🚫 Error!")
        return
    
    print("✅ Done.")  

################################################################################################
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
    cnt1 = 0

    while True:
        if cnt1 > 5: break
        flag = None
        try:
            driver.get(pUrl)
            wait = WebDriverWait(driver, 10)

            scroll(driver, wait)
            flag = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.shopee-product-rating")))
            
        except TimeoutException as e:
            cnt1 += 1
            continue
        finally:
            while True:
                if flag is not None:
                    reviews = driver.find_elements_by_css_selector("div.shopee-product-rating")
                    
                    if type(reviews) == list:
                        for review in reviews:
                            comment = review.find_element_by_class_name("shopee-product-rating__content").text
                            rating = len(review.find_elements_by_class_name("icon-rating-solid--active"))
                            
                            new_review = Review(comment, rating)
                            customers_reviews.append(new_review)
                    
                    flag1 = None
                    cnt = 0
                    while True:
                        flag1 = None
                        
                        if cnt > 5: 
                            stop = True
                            break
                        
                        try:
                            flag1 = wait.until(EC.element_to_be_clickable(locator_button))
                            
                            if flag1 is not None:
                                flag1.click()
                        except TimeoutException as e:
                            cnt += 1
                            continue
                        finally:
                            break
                       
                    cnt2 = 0 
                    while flag1 is not None:
                        if cnt2 > 5: break
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
                            cnt2 += 1
                            continue
                        finally:
                            break
                        
                if stop: break
                
                flag = None
                
                cnt3 = 0
                while flag is None:
                    if cnt3 > 5:
                        stop = True
                        break
                    
                    try:
                        flag = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.shopee-product-rating")))
                    except TimeoutException as e:
                        flag = None
                        cnt3 += 1
                    finally: break
                
            return customers_reviews