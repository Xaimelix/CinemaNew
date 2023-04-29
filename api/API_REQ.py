import requests
from requests import get
from pprint import pprint

API_KEY = '805ba88b-27c9-4cc6-8809-29a59803afaa'

# API_URL = 'https://kinopoiskapiunofficial.tech/api/v2.2/films/top?type=TOP_250_BEST_FILMS&page=1'
API_URL_ID = 'https://kinopoiskapiunofficial.tech/api/v2.2/films/'
API_URL_VIDEO = lambda x: f'https://kinopoiskapiunofficial.tech/api/v2.2/films/{x}/videos'


# API_URL = 'https://kinopoiskapiunofficial.tech/api/v2.2/films/435'


def get_main_page(page: int) -> dict:
    API_URL = f'https://kinopoiskapiunofficial.tech/api/v2.2/films/top?type=TOP_250_BEST_FILMS&page={page}'
    resp = get(API_URL, headers={'X-API-KEY': API_KEY,
                                 'Content-Type': 'application/json'})
    return resp.json()


def get_film_by_id(id: int) -> dict:
    resp = get(API_URL_ID + str(id), headers={'X-API-KEY': API_KEY,
                                              'Content-Type': 'application/json'})

    return resp.json()


def get_trailer(id: int) -> dict:
    url = API_URL_VIDEO(id)
    resp = get(url, headers={'X-API-KEY': API_KEY,
                             'Content-Type': 'application/json'})
    return resp.json()

