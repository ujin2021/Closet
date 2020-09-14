# 언니가 짠 추천 함수 코드

def recommendation(filtering, filtering_freq, sex, hashtag, weather) :
    print(f'{filtering}\n{filtering_freq}\n{sex}\n{hashtag}\n{weather}')

    return ['black_none_shortsleeve', 'black_none_longpants'], ['black_none_sumlongdress'], ['black_none_sleeveless', 'black_none_longpants']
    # return 값이 튜플이면 ('black_none_sumlongdress') dress 같은 경우 그냥 string으로 나와서 for 문 range err 발생하니까 list 로 바꿀수있는지