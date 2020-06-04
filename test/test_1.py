# from selenium import webdriver
# import pytest
from page_object.ChooserType import ChooserType

'''
Парсит все ссылки на матрасы с onliner.by в all_links.txt. 
Запускать только при добавление новых коллекций/типов/размеров
Время выполнения ~ 5 минут
'''

def test_1(browser):
    matras = ChooserType(browser)
    matras.get_matras_page()
    matras.get_all_link_in_cycle()
