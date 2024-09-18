from abc import ABC, abstractmethod
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

options = webdriver.ChromeOptions()
options.add_argument("headless")

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.implicitly_wait(time_to_wait=2)
driver.maximize_window()


class BaseIterator(ABC):
    def __iter__(self):
        return self

    @abstractmethod
    def __next__(self):
        pass


class MusinsaIterator(BaseIterator):
    BASE_URL = "https://www.musinsa.com/category/003004?sale_goods=&color=&d_cat_cd=003004&plusDeliveryYn=&sort=pop_category&timesale_yn=&tags=&list_kind=small&shoeSizeOption=&measure=&includeKeywords=&sub_sort=&exclusive_yn=&group_sale=&ex_soldout=&page=3&brand=&price1=&campaign_id=&display_cnt=90&kids=&price2=&gf=A"
    PRODUCT_ATTRIBUTE_XPATH = '//*[@id="commonLayoutContents"]/div[3]/div/div/div/div[1]/div/div[{col}]/div[2]/div/div[1]/a[2]'
    PAGE_ATTRIBUTE_XPATH = '//*[@id="commonLayoutContents"]/div[3]/div/div/div/div[1]'

    def __init__(self, driver, max_iter=50, n_col=3):
        self.driver = driver
        self.driver.get(self.BASE_URL)
        self.max_iter = max_iter
        self.n_col = n_col
        self.product_ids = set()
        self.__page_init()

    def __next__(self):
        try:
            if self.n_products >= self.max_iter:
                raise StopIteration
            product = self.get_product()
            if product["product_id"] in self.product_ids:
                raise NoSuchElementException
            self.product_ids.add(product["product_id"])
            return product
        except NoSuchElementException:
            self.next_page()
            return self.__next__()

    def next_page(self):
        self.cur_height += self.page_height
        self.driver.execute_script(f"window.scrollTo(0, {self.cur_height})")
        time.sleep(1.0)  # wait for loading

    def get_product(self):
        col = self.n_products % self.n_col + 1
        attribute = self.driver.find_element(
            By.XPATH, self.PRODUCT_ATTRIBUTE_XPATH.format(col=str(col))
        )
        return {
            "product_id": attribute.get_attribute("data-item-list-index"),
            "brand": attribute.get_attribute("data-brand-id"),
            "name": attribute.find_element(By.XPATH, "span").text,
            "price": attribute.get_attribute("data-price"),
        }

    def __page_init(self):
        self.page_attribute = self.driver.find_element(
            By.XPATH, self.PAGE_ATTRIBUTE_XPATH
        )
        self.page_height = int(self.page_attribute.get_attribute("data-known-size"))
        self.cur_height = self.driver.execute_script("return window.scrollY")
        self.cur_height += self.page_height

    def has_next(self):
        return self.n_products < self.max_iter

    @property
    def n_products(self):
        return len(self.product_ids)


class WConceptIterator(BaseIterator):
    BASE_URL = "https://display.wconcept.co.kr/category/women/001001?page={page}"
    BASE_XPATH = '//*[@id="container"]/div/div/div[3]/div/section/div[3]/div'

    def __init__(self, driver, max_iter=50):
        self.driver = driver
        self.max_iter = max_iter
        self.n_iter = 0
        self.page = 1
        self.elements = []

    def __next__(self):
        try:
            if self.n_iter >= self.max_iter:
                raise StopIteration
            product = self.get_product(self.elements.pop(0))
        except (IndexError, NoSuchElementException):
            self.next_page()
            return self.__next__()
        self.n_iter += 1
        return product

    def get_product(self, element):
        return {
            "brand": element.find_element(By.CLASS_NAME, "title").text,
            "name": element.find_element(By.CLASS_NAME, "detail").text,
            "price": element.find_element(By.CLASS_NAME, "final-price").text,
        }

    def has_next(self):
        return self.n_iter < self.max_iter

    def next_page(self):
        BASE_URL = self.BASE_URL.format(page=str(self.page))
        self.driver.get(BASE_URL)
        self.elements = self.driver.find_element(
            By.XPATH, self.BASE_XPATH
        ).find_elements(By.CLASS_NAME, "area-info")
        self.page += 1


class Application:
    def create_iterator(self, site):
        if site == "musinsa":
            return MusinsaIterator(driver, max_iter=50)
        elif site == "wconcept":
            return WConceptIterator(driver, max_iter=100)
        else:
            raise ValueError(f"Invalid site: {site}")

    def run(self):
        self.get_products(site="musinsa")
        self.get_products(site="wconcept")

    def get_products(self, site):
        iterator = self.create_iterator(site)
        products = []
        for product in iterator:
            products.append(product)
            print(product)
        self.save(products, site)

    def save(self, products, file_name):
        import pandas as pd

        pd.DataFrame(products)[["brand", "name", "price"]].to_csv(
            f"{file_name}.csv", index=False
        )


app = Application()
app.run()
