from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
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
class Review:
    def __init__(self, pComment, pRating):
        self.iComment = pComment
        self.iRating = pRating
        
def scroll(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    new_height = driver.execute_script("return document.body.scrollHeight")

    while new_height != last_height:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "footer")))
        last_height = new_height
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        new_height = driver.execute_script("return document.body.scrollHeight")
        
def getAllReviewsOfProduct(pProductURL: str, pCommentPattern: str=None, pRatingPattern: str=None):
    driver = webdriver.Firefox()
    driver.get(pProductURL)
    scroll(driver)
    
    last_pagi = 1
    new_pagi = 1
    reviews = []
    wait = WebDriverWait(driver, 10)
        
    reviews = driver.find_elements_by_css_selector("div.shopee-product-rating")

    for review in reviews:
        comment = review.find_element_by_css_selector("div.shopee-product-rating__content").text
        rating = len(review.find_elements_by_css_selector("svg.icon-rating-solid--active"))
        new_review = Review(comment, rating)
        reviews.append(new_review)
    
    
    while True:
        try:
            last_pagi = new_pagi      
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.shopee-icon-button--right"))).click() 
            new_pagi = int(driver.find_element_by_css_selector("button.shopee-button-solid--primary").text) 
            
            if new_pagi == last_pagi:
                break
            
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.shopee-product-rating")))    
            reviews = driver.find_elements_by_css_selector("div.shopee-product-rating")
            
            for review in reviews:
                comment = review.find_element_by_css_selector("div.shopee-product-rating__content").text
                rating = len(review.find_elements_by_css_selector("svg.icon-rating-solid--active"))
                print(f"{comment} {rating}")
                new_review = Review(comment, rating)
                reviews.append(new_review)
        except:
            pass
        
    
    driver.close()
    driver.quit()
    return reviews
      
        