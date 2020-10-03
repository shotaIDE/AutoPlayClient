from django.conf import settings
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from api.twitter import favorite, search, user
from api.twitter.user import (ACCESS_SECRET_KEY, ACCESS_TOKEN_KEY,
                              CREDENTIALS_SOURCE, UID_KEY, CredentialsSource)


@csrf_exempt
def search_2hDTM(request):
    consumer_key = settings.TWITTER_CONSUMER_KEY
    consumer_secret = settings.TWITTER_CONSUMER_SECRET

    user_secret = user.get_credentials(request)
    access_token = user_secret[ACCESS_TOKEN_KEY]
    access_secret = user_secret[ACCESS_SECRET_KEY]
    credentials_source = user_secret[CREDENTIALS_SOURCE]

    result = search.hashtag_2hDTM(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_secret=access_secret,
        gae_hosting=settings.GAE_HOSTING)

    # 配列をJSONに変換するために、safe を False にしておく
    response = JsonResponse(result, safe=False)

    if credentials_source == CredentialsSource.DB:
        # 旧方式のDBによる秘匿情報の取得を実施した場合は、新方式のCookieに移植
        user.set_credentials(
            response=response,
            access_token=access_token,
            access_secret=access_secret)

    return response


@csrf_exempt
def create_user(request):
    user_credentials = user.get_credentials_on_create(request=request)
    uid = user_credentials[UID_KEY]
    access_token = user_credentials[ACCESS_TOKEN_KEY]
    access_secret = user_credentials[ACCESS_SECRET_KEY]

    print(
        'User accound was received: '
        f'UID={uid}, AccessToken={access_token}, Secret={access_secret}')

    http_response = HttpResponse()
    user.set_credentials(
        response=http_response,
        access_token=access_token,
        access_secret=access_secret)

    return http_response


@csrf_exempt
def create_favorite(request):
    consumer_key = settings.TWITTER_CONSUMER_KEY
    consumer_secret = settings.TWITTER_CONSUMER_SECRET

    target_id = request.POST.get('id')

    user_secret = user.get_credentials(request)
    access_token = user_secret[ACCESS_TOKEN_KEY]
    access_secret = user_secret[ACCESS_SECRET_KEY]

    result = favorite.create(
        id=target_id,
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_secret=access_secret)

    if result == favorite.PostResult.SUCCEED:
        return JsonResponse({})

    if result == favorite.PostResult.ALREADY_FAVORITED:
        return JsonResponse(
            {
                'code': 139,
                'message': 'already favorited'
            })

    return HttpResponse(status=403)
