import json
import pytest
import keyword
import itertools
from colorama import init, Fore, Back, Style

def json_open(file_name: str):
    with open(file_name, "r", encoding="utf-8") as json_data:
        try:
            json_object = json.load(json_data)
        except ValueError as e:
            return False
        json_data.close()
        return json_object



class ColorizeMixin(object):
    def __repr__(self):
        return f'\033[0;', ';49m', '\033[0;39;48m'

class Advert:
    def __init__(self,response):
         self.price = 0
         self.repr_color_code = 32
         for k,v in response.items():
            if keyword.iskeyword(k):
                nkey = k + '_'
            else:
                nkey = k
            if isinstance(v,dict):
                self.__dict__[nkey] = Advert(v)
            else:
                if nkey == 'price':
                    self.price = response[k]
                else:
                    self.__dict__[nkey] = v

    #contextual getter
    @property
    def price(self):
        return self._price

    #contextual setter
    @price.setter
    def price(self, new_price):
        if new_price < 0:
            raise ValueError
        else:
            self._price = new_price


    def __repr__(self):
        color = ColorizeMixin.__repr__(self)
        try:
            return color[0] + f'{self.repr_color_code}' + color[1] +\
                f'{self.title} | {self.price} ₽' + color[2]
        except AttributeError:
            return 'В объекте нет необходимого аттрибута'


def test_iphone_location():
    """
    Тест на обращение во вложенный объект
    """
    iphone_ad = Advert(json_open('jsons/iphone.json'))
    assert iphone_ad.location.address == "город Самара, улица Мориса Тореза, 50"


def test_iphone_wrong_price():
    """
    Тест на неправильную цену
    """
    with pytest.raises(ValueError):
        Advert(json_open('jsons/iphone_wrong_price.json'))


def test_iphone_no_price():
    """
    Тест на отсутствие цены
    """
    iphone_ad = Advert(json_open('jsons/iphone_noprice.json'))
    assert iphone_ad.price == 0


def test_corgi_keyword():
    """
    Тест на существование аттрибута
    """
    corgi_ad = Advert(json_open('jsons/corgi.json'))
    assert corgi_ad.class_ == 'dogs'


def test_corgi_notitle():
    """
    Тест отсутвия аттрибута
    """
    corgi_ad = Advert(json_open('jsons/corgi_no_title.json'))
    assert f'{corgi_ad}' == 'В объекте нет необходимого аттрибута'


def test_color():
    """
    Тест изменения цвета
    """
    corgi_ad = Advert(json_open('jsons/corgi.json'))
    iphone_ad = Advert(json_open('jsons/iphone.json'))
    assert f'{corgi_ad}' == '\033[0;32;49mВельш-корги | 1000 ₽\033[0;39;48m' and f'{iphone_ad}' == '\033[0;32;49miPhone X | 100 ₽\033[0;39;48m'
