import json
import requests
TMDB_API_KEY = '94cfb0b050444c186251cd8dee48a17d'

movie_id = []


def get_movie_datas():
    total_data = []
    # 1페이지부터 500페이지까지 (페이지당 20개, 총 10,000개)
    for i in range(1, 50):
        request_url = f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&language=ko-KR&page={i}"
        movies = requests.get(request_url).json()

        for movie in movies['results']:
            if movie.get('adult') == False and movie.get('release_date', ''):
                fields = {
                    'movie_id': movie['id'],
                    'title': movie['title'],
                    'released_date': movie['release_date'],
                    'popularity': movie['popularity'],
                    'vote_avg': movie['vote_average'],
                    'overview': movie['overview'],
                    'poster_path': movie['poster_path'],
                    'backdrop_path': movie['backdrop_path'],
                    'genres': movie['genre_ids']
                }

                data = {
                    "pk": movie['id'],
                    "model": "movies.movie",
                    "fields": fields
                }
                movie_id.append(movie['id'])
                total_data.append(data)

    with open("movie.json", "w", encoding="utf-8") as w:
        json.dump(total_data, w, indent="\t", ensure_ascii=False)


def get_credit_datas():
    total_data = []
    for mid in movie_id:
        request_url = f"https://api.themoviedb.org/3/movie/{mid}/credits?api_key={TMDB_API_KEY}&language=ko-KR"
        get_credits = requests.get(request_url).json()
        for credit in get_credits['cast']:
            if credit.get('popularity') > 5 and credit.get('profile_path') != '':
                fields = {
                    'person_id': credit['id'],
                    "movie_id": mid,
                    'name': credit['name'],
                    'popularity': credit['popularity'],
                    'character': credit['character'],
                    'profile_path': credit['profile_path'],
                }
                data = {
                    'model': "movies.credit",
                    "fields": fields
                }
                total_data.append(data)
    print(len(total_data))
    with open("credit.json", "w", encoding="utf-8") as w:
        json.dump(total_data, w, indent="\t", ensure_ascii=False)


def get_video_datas():
    total_data = []
    for mid in movie_id:
        request_url = f"https://api.themoviedb.org/3/movie/{mid}/videos?api_key={TMDB_API_KEY}&language=ko-KR"
        get_videos = requests.get(request_url).json()
        for video in get_videos['results']:
            fields = {
                'key': video['key'],
                "movie_id": mid,
                'iso_639_1': video['iso_639_1'],
                'iso_3166_1': video['iso_3166_1'],
                'name': video['name'],
                'site': video['site'],
                'video_id': video['id'],
                'published_at': video['published_at'],
            }
            data = {
                'model': "movies.video",
                "fields": fields
            }
            total_data.append(data)
    print(len(total_data))
    with open("video.json", "w", encoding="utf-8") as w:
        json.dump(total_data, w, indent="\t", ensure_ascii=False)


get_movie_datas()
get_credit_datas()
get_video_datas()
