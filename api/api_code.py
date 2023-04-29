from api.API_REQ import get_main_page, get_film_by_id
import pprint
from pprint import pprint


def get_genres():
    answer = set()
    for num in range(1, 18):
        for i in get_main_page(num)['films']:
            # print(get_film_by_id(i['filmId'])['genres'])
            for k in get_film_by_id(i['filmId'])['genres']:
                answer.add(k['genre'])
    return list(answer)


def get_films():
    answer = list()
    for n in range(1, 18):
        for i in get_main_page(n)['films']:
            answer.append(get_film_by_id(i['filmId']))
            # pprint(get_film_by_id(i['filmId']))
            break
    return answer


# pprint(get_genres())
# pprint(get_films())
# for element in answer:
#     print(
#         f'id: {element["kinopoiskId"]}, name: {element["nameRu"]}, dur: {element["filmLength"]}, year: {element["year"]},'
#         f' description: {element["description"]}, genres: {element["genres"]}')
