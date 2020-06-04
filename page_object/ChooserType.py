# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from id.id import SellerId


class ChooserType:
    def __init__(self, driver):
        self.driver = driver

    def group_selectors(self):  # селекторы на каждый тип
        return self.driver.find_elements_by_css_selector('div[class="schema-product__group"]')

    def get_all_selector_child(self, element):  # селекторы на каждый размер одного типа
        self.element = element
        return self.element.find_elements_by_css_selector('div[class="schema-product schema-product_children"]')

    def get_matras_page(self):
        return self.driver.get('https://catalog.onliner.by/mattress/eos/')

    def get_card_page(self, link):
        return self.driver.get(link + '?order=price:desc&town_id=17030')  # сразу выбираем город и сортировку по цене

    def get_attr(self, element):
        self.element = element
        self.name = self.element.find_element_by_css_selector('span[data-bind*=".extended_name"]')
        name = self.name.text
        return name

    def see_more(self, element):
        #  в некоторых случаях (типа детские матрасы) кнопки "посмотреть все размеры" нет
        try:
            self.element = element
            see_more = self.element.find_element_by_css_selector('.schema-product__more-control a')
            see_more.click()
        except:
            pass

    def get_min_price(self, element):
        self.element = element
        min_price = self.element.find_element_by_css_selector('.schema-product__price span')
        return min_price.text

    def get_link(self, element):
        self.element = element
        link = self.element.find_element_by_css_selector('.schema-product__price a')
        return link.get_attribute('href')

    def get_all_link_in_cycle(self):
        list_of_one_type = []
        for selector in self.group_selectors():  # разбиваем все на блоки для ускорения работы

            self.see_more(selector)  # кнопка "посмотреть все размеры"

            for child_selector in self.get_all_selector_child(selector):  # здесь разные размеры одного типа

                print(self.get_link(child_selector))
                list_of_one_type.append(self.get_link(child_selector)+'\n')
            self.see_more(selector)  # кнопка "посмотреть все размеры"

        for string in list_of_one_type:
            open('all_links.txt', 'a').writelines(string)

    def is_demp(self):  # единая ли цена у всех?
        if '–' in self.driver.find_element_by_css_selector('span[class="helpers_hide_tablet"]').text:
            return True
        else:
            return False

    def get_all_price(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((
            By.CSS_SELECTOR, 'tr[data-bind*="position.data.is_highlight_promotion_winner"]')))
        links = self.driver.find_elements_by_css_selector(
            'tr[data-bind*="position.data.is_highlight_promotion_winner"]')  # селекторы всех магазинов
        price_list = []

        for link in links:
            self.link = link
            price = self.link.find_element_by_css_selector('span[data-bind*="position.format.priceObject"]').text
            price_list.append(price)
            seller_id = self.link.find_element_by_css_selector('a[class="logo"]').get_attribute('href')
            seller_id = re.findall(r'(?<=["https://"]{8})\d{1,6}(?=[".shop.onliner.by"])', seller_id)[0]

            if price != price_list[0]:  # если цена не правильная, пишем в лог
                self.write_log(seller_id, price, price_list[0])

    def write_log(self, id_seller, price, price_rrc):

        title = self.driver.title[4:-13]
        link = self.driver.current_url
        seller_name = self.seller_name_from_id(id_seller)
        with open(f'../log/{seller_name}.txt', 'a') as f:
            f.writelines(f'{title} -- {link} -- {seller_name} -- цена факт={price} -- цена РРЦ={price_rrc}\n')

    @staticmethod
    def seller_name_from_id(id_seller):
        try:  # если данного магазина не знаем, то пишем в лог его id
            return SellerId.seller_id[id_seller]
        except:
            return id



