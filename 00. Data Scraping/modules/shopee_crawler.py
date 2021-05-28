from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
    

def loadProductsURL(pUrlPattern: str, pRange, pProductPattern):
    driver = webdriver.Firefox()
    products_url = []
    
    for i in range(pRange[0], pRange[1]):
        url = f"{pUrlPattern}{i}"
        driver.get(url)
        last_height = driver.execute_script("return document.body.scrollHeight") # chiều cao ban đầu của trang
        
        while True:
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # lặn chuột xuống cuối trang
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "footer"))) # chờ AJAX gửi data về trong tối đa 10 giây và chờ thẻ `footer` xuất hiện
                new_height = driver.execute_script("return document.body.scrollHeight") # lấy chiều cao hiện tại của trang
                
                if new_height != last_height: continue # thẻ `footer` chưa xuất hiện
            finally:
                break # thẻ `footer` xuất hiện nên rời khỏi trang
    
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
        