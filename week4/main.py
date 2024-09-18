from abc import ABC, abstractmethod
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException


def load_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.implicitly_wait(time_to_wait=2)
    driver.maximize_window()
    return driver


class BaseIterator(ABC):
    @abstractmethod
    def __next__(self):
        pass


class MusinsaIterator(BaseIterator):
    BASE_URL = "https://www.musinsa.com/category/{category}?sale_goods=&color=&d_cat_cd={category}&plusDeliveryYn=&sort=pop_category&timesale_yn=&tags=&list_kind=small&shoeSizeOption=&measure=&includeKeywords=&sub_sort=&exclusive_yn=&group_sale=&ex_soldout=&page=3&brand=&price1=&campaign_id=&display_cnt=90&kids=&price2=&gf=A"
    PRODUCT_ATTRIBUTE_XPATH = '//*[@id="commonLayoutContents"]/div[3]/div/div/div/div[1]/div/div[{col}]/div[2]/div/div[1]/a[2]'
    PAGE_ATTRIBUTE_XPATH = '//*[@id="commonLayoutContents"]/div[3]/div/div/div/div[1]'

    def __init__(self, driver, category: str, max_iter=50, n_col=3):
        self.driver = driver
        self.driver.get(self.BASE_URL.format(category=category))
        self.max_iter = max_iter
        self.n_col = n_col
        self.product_ids = set()
        self._init_page()
        self.elements = []

    def __iter__(self):
        return self

    def __next__(self):
        try:
            if self.n_products >= self.max_iter:
                raise StopIteration
            product = self.get_product(self.elements.pop(0))
            if product["product_id"] in self.product_ids:
                raise NoSuchElementException
            self.product_ids.add(product["product_id"])
            return product
        except (IndexError, NoSuchElementException):
            self.next_page()
            return self.__next__()

    def next_page(self):
        self.cur_height += self.page_height
        self.driver.execute_script(f"window.scrollTo(0, {self.cur_height})")
        self.elements = [
            self.driver.find_element(
                By.XPATH, self.PRODUCT_ATTRIBUTE_XPATH.format(col=str(i))
            )
            for i in range(1, self.n_col + 1)
        ]
        time.sleep(1.0)

    def get_product(self, element):
        return {
            "product_id": element.get_attribute("data-item-list-index"),
            "brand": element.get_attribute("data-brand-id"),
            "name": element.find_element(By.XPATH, "span").get_attribute("innerText"),
            "price": element.get_attribute("data-price"),
        }

    def _init_page(self):
        self.page_attribute = self.driver.find_element(
            By.XPATH, self.PAGE_ATTRIBUTE_XPATH
        )
        self.page_height = int(self.page_attribute.get_attribute("data-known-size"))
        self.cur_height = self.driver.execute_script("return window.scrollY")
        self.cur_height += self.page_height

    @property
    def n_products(self):
        return len(self.product_ids)


class WConceptIterator(BaseIterator):
    BASE_URL = "https://display.wconcept.co.kr/category/women/{category}?page={page}"
    BASE_XPATH = '//*[@id="container"]/div/div/div[3]/div/section/div[3]/div'

    def __init__(self, driver, category: str, max_iter=50):
        self.driver = driver
        self.driver.get(self.BASE_URL.format(category=category))
        self.category = category
        self.max_iter = max_iter
        self.n_iter = 0
        self.page = 1
        self.elements = []

    def __iter__(self):
        return self

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

    def next_page(self):
        BASE_URL = self.BASE_URL.format(
            category=str(self.category), page=str(self.page)
        )
        self.driver.get(BASE_URL)
        self.elements = self.driver.find_element(
            By.XPATH, self.BASE_XPATH
        ).find_elements(By.CLASS_NAME, "area-info")
        self.page += 1


class Application:
    def __init__(self, site: str, category: str):
        self.site = site
        self.category = category

    @staticmethod
    def create_iterator(site, category):
        if site == "musinsa":
            driver = load_driver()
            return MusinsaIterator(driver, category, max_iter=50)
        elif site == "wconcept":
            driver = load_driver()
            return WConceptIterator(driver, category, max_iter=100)
        else:
            raise ValueError(f"Invalid site: {site}")

    def run(self):
        self.get_products(site=self.site, category=self.category)

    def get_products(self, site, category):
        iterator = self.create_iterator(site, category)
        products = []
        for product in iterator:
            products.append(product)
            print(product)
        self.save(products, site)

        iterator.driver.quit()
        del iterator

    def save(self, products, file_name):
        import pandas as pd

        pd.DataFrame(products)[["brand", "name", "price"]].to_csv(
            f"{file_name}.csv", index=False
        )


if "__main__" == __name__:
    import argparse

    args = argparse.ArgumentParser()
    args.add_argument(
        "--site", type=str, default="musinsa", help="site name e.g. musinsa, wconcept"
    )
    args.add_argument(
        "--category",
        type=str,
        default="003004",
        help="category id e.g. (musinsa: 003004), (wconcept: 001001)",
    )
    args = args.parse_args()

    app = Application(site=args.site, category=args.category)
    app.run()
