from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404, get_list_or_404
from .models import Movie, Genre, Credit, Comment, ClickedMovies, Video, UnseenMovies
from .serializers import MovieListSerializer, ActorSerializer, MovieSerializer, CommentSerializer, ClickedMovieSerializer, VideoSerializer, UnseenMovieSerializer
import random
import numpy as np

# Create your views here.

# -----------------------------------------------------------
# 비로그인 메인 페이지
# 투표 내림차순 (비로그인)


@api_view(['GET'])
def movie_list_voted(request):
    if request.method == 'GET':
        movies = get_list_or_404(Movie)
        voted_movies = []
        for movie in movies:
            if movie.vote_avg > 5:
                voted_movies.append(movie)
        voted_movies = sorted(voted_movies, key=lambda x: -x.vote_avg)
        voted_movies150 = voted_movies[:150]
        voted_movies30 = random.sample(voted_movies150, 30)
        serializer = MovieListSerializer(voted_movies30, many=True)
        return Response(serializer.data)


# 고전명작 (비로그인)
@api_view(['GET'])
def movie_list_old(request):
    if request.method == 'GET':
        movies = get_list_or_404(Movie)
        old_movies = []
        for movie in movies:
            if movie.vote_avg > 5:
                old_movies.append(movie)
        old_movies = sorted(old_movies, key=lambda x: x.released_date)
        old_movies30 = old_movies[:30]

        serializer = MovieListSerializer(old_movies30, many=True)
        return Response(serializer.data)


# 인기도 내림차순 (비로그인)
@api_view(['GET'])
def movie_list_popular(request):
    if request.method == 'GET':
        movies = get_list_or_404(Movie)
        popular_movies = []
        for movie in movies:
            if movie.vote_avg > 5:
                popular_movies.append(movie)
        popular_movies = sorted(popular_movies, key=lambda x: -x.popularity)
        popular_movies30 = popular_movies[:30]

        serializer = MovieListSerializer(popular_movies30, many=True)
        return Response(serializer.data)

# ------------------------------------------------------------------------------
# 로그인 후 메인 페이지

# 내가 클릭한거 중에서 안보고 싶은거 뺀 함수 (여기저기에서 다 사용할거임,,,)


def get_user_clicked(user_id):
    clicked_movies = get_list_or_404(ClickedMovies)
    # unseen_movies = get_list_or_404(UnseenMovies)
    unseen_movies = UnseenMovies.objects.all()
    # 내가 클릭한 영화
    user_clicked_movies = list(
        filter(lambda x: x.user_id == user_id, clicked_movies))
    # 내가 안보고 싶다고 누른 영화
    user_unseen_movies = list(
        filter(lambda x: x.user_id == user_id, unseen_movies))
    # 내가 클릭한 거랑 안보고 싶은거 비교하면서 movie_id 달라야지만 넣기
    user_clicked_movies1 = []
    for movie in user_clicked_movies:
        if movie not in user_unseen_movies:
            user_clicked_movies1.append(movie)

    # 영화의 정보까지 가져오기
    movies = get_list_or_404(Movie)
    user_clicked_movie_info = []
    for clicked_movie in user_clicked_movies:
        for movie in movies:
            if clicked_movie.movie_id == movie.movie_id:
                user_clicked_movie_info.append(movie)

    user_clicked_movie_info.reverse()
    return user_clicked_movie_info


# 전체 영화 중에서 내가 안보고 싶다고 클릭한거 뺀 함수 (여기저기에서 다 쓸거임,,,)
def get_user_candidates(user_id):
    movies = get_list_or_404(Movie)
    unseen_movies = UnseenMovies.objects.all()
    # unseen_movies = get_list_or_404(UnseenMovies)
    user_unseen_movies = list(
        filter(lambda x: x.user_id == user_id, unseen_movies))
    # 내가 안보고 싶은거랑 영화랑 비교하면서 제목 달라야지만 넣기
    user_recommend_candidates = []
    for movie in movies:
        flg = 0
        for unseen_movie in user_unseen_movies:
            if movie.movie_id == unseen_movie.movie_id:
                flg += 1
            else:
                continue

        if flg != 0:
            continue
        else:
            user_recommend_candidates.append(movie)

    return user_recommend_candidates


# 내가 클릭한 영화 최신순
@api_view(['GET'])
def movie_list_clicked(request, user_id):
    if request.method == 'GET':
        # print('qwdopqwkdpowqkdpo')
        # print('qwdopqwkdpowqkdpo')
        # print('qwdopqwkdpowqkdpo')
        # print('qwdopqwkdpowqkdpo')
        show_movies = get_user_clicked(user_id)
        result = []
        for show_movie in show_movies:
            if show_movie not in result:
                result.append(show_movie)
        result30 = result[:30]
        serializer = MovieListSerializer(result30, many=True)
        return Response(serializer.data)


# 내가 클릭한거 기반 장르 알고리즘
@api_view(['GET'])
def movie_list_genre_recommend(request, user_id):
    if request.method == 'GET':
        clicked_movies_info = get_user_clicked(user_id)
        movies = get_user_candidates(user_id)
        # 중복제거
        user_clicked_movies_unique = []
        for clicked_movie_info in clicked_movies_info:
            if clicked_movie_info not in user_clicked_movies_unique:
                user_clicked_movies_unique.append(clicked_movie_info)
        bucket = [0]*len(user_clicked_movies_unique)
        # 해당 사용자가 클릭 더 많이 할수록 가중치
        for i in range(len(user_clicked_movies_unique)):
            for j in range(len(clicked_movies_info)):
                if user_clicked_movies_unique[i] == clicked_movies_info[j]:
                    bucket[i] += 1
                    break
        # 장르 같으면 가중치 추가
        movies_bucket = [0]*len(movies)
        for i in range(len(user_clicked_movies_unique)):
            # for j in clicked_movies_info[i].genres.all():
            for k in range(i, len(movies)):
                # for l in movies[k].genres.all():
                if len(list(movies[k].genres.all())) > 0 and len(list(movies[k].genres.all())) > 0:
                    if clicked_movies_info[i].genres.all()[0] == movies[k].genres.all()[0]:
                        movies_bucket[k] += bucket[i]
                else:
                    continue
        prob = []
        for p in movies_bucket:
            prob.append(p/sum(movies_bucket))
        result = np.random.choice(movies, size=30, replace=False, p=prob)
        serializer = MovieListSerializer(result, many=True)
        return Response(serializer.data)


# 유사도측정(유클리디안 거리)
@api_view(['GET'])
def movie_list_euclidean_recommend(request, user_id):
    clicked_movies_info = get_user_clicked(user_id)
    movies = get_user_candidates(user_id)
    # 클릭한 영화 중복제거
    user_clicked_movies_unique = []
    for clicked_movie_info in clicked_movies_info:
        if clicked_movie_info not in user_clicked_movies_unique:
            user_clicked_movies_unique.append(clicked_movie_info)
    # 클릭한 영화의 인기도랑 투표수만 가져와서 배열에 넣기
    user_clicked_movies_numbers = []
    for user_clicked_movie_unique in user_clicked_movies_unique:
        user_clicked_movies_numbers.append(
            [user_clicked_movie_unique.vote_avg, user_clicked_movie_unique.popularity])
    # 모든 영화의 인기도랑 투표수만 가져와서 배열에 넣기
    movies_numbers = []
    for movie in movies:
        movies_numbers.append([movie.vote_avg, movie.popularity])
    # 유클리디안 거리 구하기
    euc = []
    for i in range(len(user_clicked_movies_numbers)):
        for j in range(i, len(movies_numbers)):
            temp = []
            dist = ((movies_numbers[j][0]-user_clicked_movies_numbers[i][0])**2 + (
                movies_numbers[j][1]-user_clicked_movies_numbers[i][1])**2)**(1/2)
            if dist != 0:
                temp.append(dist)
                temp.append(movies[j])
                euc.append(temp)
    euc = sorted(euc, key=lambda x: x[0])
    # 중복 없애기
    result = []
    for e in euc:
        if e[1] not in result:
            result.append(e[1])

    result30 = result[:30]
    serializer = MovieListSerializer(result30, many=True)
    return Response(serializer.data)


# 로그인 후 투표순 리스트
@api_view(['GET'])
def personal_movie_list_voted(request, user_id):
    if request.method == 'GET':
        isUnseen = UnseenMovies.objects.all()
        voted_movies = []
        if len(isUnseen) == 0:
            movies = get_list_or_404(Movie)
            for movie in movies:
                if movie.vote_avg > 5:
                    voted_movies.append(movie)
        else:
            # 해당 사용자가 클릭한 영화만 뽑아서 user_unseen_movies 에 넣기
            movies = get_user_candidates(user_id)
            unseen_movies = get_list_or_404(UnseenMovies)
            user_unseen_movies = list(
                filter(lambda x: x.user_id == user_id, unseen_movies))
            for movie in movies:
                if movie.vote_avg > 5:
                    if movie not in user_unseen_movies:
                        voted_movies.append(movie)
        voted_movies = sorted(voted_movies, key=lambda x: -x.vote_avg)
        voted_movies150 = voted_movies[:150]
        voted_movies30 = random.sample(voted_movies150, 30)
        serializer = MovieListSerializer(voted_movies30, many=True)
        return Response(serializer.data)

# 로그인 후 고전명작 리스트


@api_view(['GET'])
def personal_movie_list_old(request, user_id):
    if request.method == 'GET':
        isUnseen = UnseenMovies.objects.all()

        if len(isUnseen) == 0:
            movies = get_list_or_404(Movie)
            old_movies = []
            for movie in movies:
                if movie.vote_avg > 5:
                    old_movies.append(movie)
        else:
            movies = get_user_candidates(user_id)
            unseen_movies = get_list_or_404(UnseenMovies)
            user_unseen_movies = list(
                filter(lambda x: x.user_id == user_id, unseen_movies))
            old_movies = []
            for movie in movies:
                if movie.vote_avg > 5:
                    if movie not in user_unseen_movies:
                        old_movies.append(movie)

        old_movies = sorted(old_movies, key=lambda x: x.released_date)
        old_movies150 = old_movies[:150]
        old_movies30 = random.sample(old_movies150, 30)
        serializer = MovieListSerializer(old_movies30, many=True)
        return Response(serializer.data)

# 로그인 후 인기순 리스트


@api_view(['GET'])
def personal_movie_list_popular(request, user_id):
    if request.method == 'GET':
        isUnseen = UnseenMovies.objects.all()

        if len(isUnseen) == 0:
            movies = get_list_or_404(Movie)
            popular_movies = []
            for movie in movies:
                if movie.vote_avg > 5:
                    popular_movies.append(movie)
        else:
            movies = get_user_candidates(user_id)
            unseen_movies = get_list_or_404(UnseenMovies)
            user_unseen_movies = list(
                filter(lambda x: x.user_id == user_id, unseen_movies))
            popular_movies = []
            for movie in movies:
                if movie.vote_avg > 5:
                    if movie not in user_unseen_movies:
                        popular_movies.append(movie)
        popular_movies = sorted(popular_movies, key=lambda x: -x.popularity)
        popular_movies150 = popular_movies[:150]
        popular_movies30 = random.sample(popular_movies150, 30)
        serializer = MovieListSerializer(popular_movies30, many=True)
        return Response(serializer.data)

# ----------------------------------------------------------------
# 디테일페이지

# 영화에 출연한 배우들 가져오기


@api_view(['GET'])
def actor_list(request, movie_id):
    if request.method == 'GET':
        actors = get_list_or_404(Credit, movie=movie_id)
        actors_5 = actors[:10]
        serializer = ActorSerializer(actors_5, many=True)
        return Response(serializer.data)

# 영화 디테일 페이지로 가기 (GET)
# 클릭한 영화 리스트에 추가하기 (POST)


@api_view(['GET', 'POST'])
def movie_detail(request, movie_id):
    # article = Article.objects.get(pk=article_pk)
    print(request)
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.method == 'GET':
        serializer = MovieSerializer(movie)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = ClickedMovieSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(movie=movie)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


# 개별 영화 트레일러
@api_view(['GET'])
def movie_detail_video(request, movie_id):
    video = get_list_or_404(Video, movie_id=movie_id)
    print(video)
    get_video = video[:1]
    print(get_video)
    if request.method == 'GET':
        serializer = VideoSerializer(get_video, many=True)
        print(serializer.data)
        return Response(serializer.data)


# 내가 디테일 페이지 들어간 영화랑 같은 장르 가진 영화들 모두 추출
@api_view(['GET'])
def movie_list_similar(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    movies = get_list_or_404(Movie)
    # 이 영화의 장르 중복없이 뽑기
    genres = []
    a = movie.genres.all()
    for b in a:
        genres.append(b.name)
    movies_recommend = []
    for genre in genres:
        for m in movies:
            g = m.genres.all()
            for i in g:
                if i.name == genre:
                    movies_recommend.append(m)
    # 중복제거 후 출력
    result = []
    for movie_recommend in movies_recommend:
        if movie_recommend not in result:
            if movie_recommend != movie:
                result.append(movie_recommend)
    result30 = result[:30]
    serializer = MovieListSerializer(result30, many=True)
    return Response(serializer.data)


# ------------------------------------------------------------------
# 커뮤니티 기능

# 해당 영화의 댓글 리스트
@api_view(['GET'])
def comment_list(request, movie_id, sort):
    if request.method == 'GET':
        comments = get_list_or_404(Comment, movie=movie_id)
        # comments.save()
        # new
        if sort == 'NEW':
            comments_new = sorted(comments, key=lambda x: -x.comment_id)
            serializer = CommentSerializer(comments_new, many=True)
        # 평점 높은 순
        elif sort == 'RATE_UP':
            comments_rate_up = sorted(comments, key=lambda x: -x.rate)
            serializer = CommentSerializer(comments_rate_up, many=True)
        # 평점 낮은 순
        elif sort == 'RATE_DOWN':
            comments_rate_down = sorted(comments, key=lambda x: x.rate)
            serializer = CommentSerializer(comments_rate_down, many=True)
        # 좋아요 순
        elif sort == 'LIKES':
            comments_likes = sorted(comments, key=lambda x: -x.likes)
            serializer = CommentSerializer(comments_likes, many=True)
        return Response(serializer.data)

        # popular_movies = sorted(
        #     popular_movies, key=lambda x: -x.popularity)


@api_view(['GET', 'DELETE', 'POST'])
def comment_like(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == 'GET':
        if request.user in comment.like_users.all():
            data = {
                'isLike': True
            }
            return Response(data)
    elif request.method == 'POST':
        comment.like_users.add(request.data['user'])
        data = {
            'success': True
        }
        return Response(data)
    elif request.method == 'DELETE':
        comment.like_users.remove(request.data['user'])
        return Response(status=status.HTTP_204_NO_CONTENT)

# 개별 댓글
# 조회 수정 삭제


@api_view(['GET', 'DELETE', 'PUT'])
def comment_detail(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)

    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


# 댓글 생성
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def comment_create(request, movie_id):
    # article = Article.objects.get(pk=article_pk)
    movie = get_object_or_404(Movie, pk=movie_id)
    # print(request.data)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        # print(request.data)
        serializer.save(movie=movie)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# 개별 댓글 좋아요
# @api_view(['GET'])
# def comment_like_list(request, comment_id):
#     if request.method == 'GET':
#         comment_likes = get_list_or_404(CommentLike, comment_id=comment_id)
#         serializer = CommentLikeSerializer(comment_likes, many=True)
#         return Response(serializer.data)


# #
# @api_view(['DELETE'])
# @permission_classes((IsAuthenticated, ))
# def comment_like_detail(request, comment_id):
#     likes = get_list_or_404(CommentLike, comment_id=comment_id)

#     if request.method == 'DELETE':
#         for like in likes:
#             if str(like.user_id) == str(request.data['user_id']):
#                 data = {
#                     'message': 'del'
#                 }
#                 like.delete()
#                 return Response(data, status=status.HTTP_204_NO_CONTENT)
# #


# @api_view(['POST'])
# @permission_classes((IsAuthenticated, ))
# def comment_like_create(request, comment_id):

#     comment = get_object_or_404(Comment, comment_id=comment_id)
#     if request.method == 'POST':
#         serializer = CommentLikeSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save(comment_id=comment)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)


# 003

# ---------------------------------------------------------------------------------------
# 안보고 싶은 영화 관련


# 안보고 싶은 영화 리스트에 추가, 삭제
@api_view(['POST', 'DELETE'])
def movie_unseen(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.method == "POST":
        serializer = UnseenMovieSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(movie=movie)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        unseen = get_list_or_404(
            UnseenMovies, movie_id=movie_id, user=request.data['user'])
        for unsee in unseen:
            if unsee.movie_id == movie.movie_id:
                a = unsee
                a.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# 이 사용자가 안보고싶어하는 영화 리스트 조회하기


@api_view(['GET'])
def movie_list_unseen(request, user_id):
    if request.method == 'GET':
        unseen_movies = get_list_or_404(UnseenMovies)
        movies = get_list_or_404(Movie)
        user_unseen_movies = []
        for unseen_movie in unseen_movies:
            if user_id == unseen_movie.user_id:
                user_unseen_movies.append(unseen_movie)

        show_movies = []
        for unseen_movie in user_unseen_movies:
            for movie in movies:
                if unseen_movie.movie_id == movie.movie_id:
                    show_movies.append(movie)

        result = []
        for show_movie in show_movies:
            if show_movie not in result:
                result.append(show_movie)

        serializer = MovieListSerializer(result, many=True)
        return Response(serializer.data)
