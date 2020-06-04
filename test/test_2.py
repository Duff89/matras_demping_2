from page_object.ChooserType import ChooserType
import sys
'''
Проверяет все цены каждого типа/размера/ткани.
Если цена не соответствует РРЦ, пишет в папку log всю инфу с сортировкой по магазину
Скрипт ориентируется на большую цену в карточке товара,
поэтому лучше не проверять в первые дни после изменения цены/акции,
чтобы все магазины успели загрузить выгрузку.
'''


def test_2(browser):
    try:
        all_matras_link = list(map(str.rstrip, open('all_links.txt').readlines()))
    except:
        print('Сначала запусти test_1 для парсинга ссылок')
        sys.exit()

    matras = ChooserType(browser)
    for link in all_matras_link:
        matras.get_card_page(link)
        if matras.is_demp():  # если есть ли демпинг, сравниваем все цены и пишем в лог
            matras.get_all_price()




