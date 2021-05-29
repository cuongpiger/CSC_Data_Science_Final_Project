from logging import shutdown

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

url = "https://shopee.vn/-M%C3%A3-FAMAYMA2-gi%E1%BA%A3m-10K-%C4%91%C6%A1n-50K-%C3%81o-thun-nam-n%E1%BB%AF-form-r%E1%BB%99ng-Yinxx-%C3%A1o-ph%C3%B4ng-tay-l%E1%BB%A1-ATL43-i.14746382.6519318270"

class Review:
    def __init__(self, pComment, pRating):
        self.iComment = pComment
        self.iRating = pRating
    
# review = driver.find_element_by_css_selector("div.shopee-product-rating").find_element_by_css_selector("div.shopee-product-rating__content").text
# review = driver.find_element_by_css_selector("div.shopee-product-rating").find_elements_by_css_selector("svg.icon-rating-solid--active")

        
        
def scroll(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    new_height = driver.execute_script("return document.body.scrollHeight")

    while new_height != last_height:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "footer")))
        last_height = new_height
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        new_height = driver.execute_script("return document.body.scrollHeight")
       
import time
        
def getAllReviewsOfProduct(pProductURL: str, pCommentPattern: str=None, pRatingPattern: str=None):
    driver = webdriver.Firefox()
    driver.get(pProductURL)
    scroll(driver)
    
    reviews = []
    wait = WebDriverWait(driver, 10)
    
    reviews = driver.find_elements_by_css_selector("div.shopee-product-rating")

    for review in reviews:
        comment = review.find_element_by_css_selector("div.shopee-product-rating__content").text
        rating = len(review.find_elements_by_css_selector("svg.icon-rating-solid--active"))
        
        print(f">> {rating} - {comment}")
        new_review = Review(comment, rating)
        reviews.append(new_review)
    
    
    while True:
        try:    
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.shopee-icon-button--right"))).click()  
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.shopee-product-rating"))) 
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.shopee-page-controller > button")))    
               
            reviews = driver.find_elements_by_css_selector("div.shopee-product-rating")
            
            for review in reviews:
                comment = review.find_element_by_css_selector("div.shopee-product-rating__content").text
                rating = len(review.find_elements_by_css_selector("svg.icon-rating-solid--active"))
                
                print(f">> {rating} - {comment}")
                new_review = Review(comment, rating)
                reviews.append(new_review)

            last_child = driver.find_elements_by_css_selector("div.shopee-page-controller > button")
        
            
            if last_child.text == driver.find_element_by_css_selector("button.shopee-button-solid--primary").text:
                break
        except:
            pass
        

    
    
    driver.close()
    driver.quit()
    return reviews


    
a = getAllReviewsOfProduct(url)
print(a[0].iComment)
