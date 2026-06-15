def solution(genres, plays):
    genre_total = {}
    genre_songs = {}

    # 1. 장르별 총 재생 수, 장르별 노래 목록 만들기
    for i in range(len(genres)):
        genre = genres[i]
        play = plays[i]

        if genre not in genre_total:
            genre_total[genre] = 0
            genre_songs[genre] = []

        genre_total[genre] += play
        genre_songs[genre].append([i, play])

    # 2. 장르를 총 재생 수 기준으로 정렬
    genre_list = list(genre_total.keys())

    def genre_sort_key(genre):
        return genre_total[genre]

    genre_list.sort(key=genre_sort_key, reverse=True)

    answer = []

    # 3. 각 장르 안에서 노래 정렬 후 최대 2개 선택
    for genre in genre_list:
        songs = genre_songs[genre]

        def song_sort_key(song):
            song_id = song[0]
            play_count = song[1]

            return [-play_count, song_id]

        songs.sort(key=song_sort_key)

        count = 0
        for song in songs:
            answer.append(song[0])
            count += 1

            if count == 2:
                break

    return answer