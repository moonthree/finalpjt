import requests
import json
import os
TMDB_API_KEY = '94cfb0b050444c186251cd8dee48a17d'

person_id = []
total_data = []


def get_person_datas():

    # 배우 만명을 불러오겠삼
    for i in range(1, 10000):
        # for i in range(1, 3):
        request_url = f"https://api.themoviedb.org/3/person/{i}?api_key={TMDB_API_KEY}&language=ko-KR"
        person = requests.get(request_url).json()

        # print(person)

        # print(person['also_known_as'])
        # print(person.id)

# #         for person in people:
# #             print(person)
# #             # print(person.id)
        if person != {'success': False, 'status_code': 34, 'status_message': 'The resource you requested could not be found.'}:
            if person['popularity'] > 5 and person.get('profile_path') != '':
                fields = {
                    'person_id': person['id'],
                    'name': person['name'],
                    'gender': person['gender'],
                    'popularity': person['popularity'],
                    'profile_path': person['profile_path'],
                    'biography': person['biography'],
                    'birthday': person['birthday'],
                    'place_of_birth': person['place_of_birth'],
                    'homepage': person['homepage'],
                }
                # print(person.id)
                data = {
                    "pk": person['id'],
                    "model": "movies.person",
                    "fields": fields
                }
                # print(data)
                person_id.append(person['id'])
                total_data.append(data)

            with open("person.json", "w", encoding="utf-8") as w:
                json.dump(total_data, w, indent="\t", ensure_ascii=False)


get_person_datas()
