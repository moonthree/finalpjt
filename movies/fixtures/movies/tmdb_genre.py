import requests
import json

TMDB_API_KEY = '94cfb0b050444c186251cd8dee48a17d'


def get_genre_datas():
    total_data = []
    # 1페이지부터 500페이지까지 (페이지당 20개, 총 5,000개)
    request_url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={TMDB_API_KEY}&language=ko-KR"
    genres = requests.get(request_url).json()
    idx = 0
    # print(genres)
    for genre in genres['genres']:
        print(genre)
        fields = {
            'genre_id': genre['id'],
            'name': genre['name']
        }

        data = {
            "pk": idx,
            "model": "movies.genre",
            "fields": fields
        }
        idx += 1
        total_data.append(data)

    with open("genre.json", "w", encoding="utf-8") as w:
        json.dump(total_data, w, indent="\t", ensure_ascii=False)


get_genre_datas()
