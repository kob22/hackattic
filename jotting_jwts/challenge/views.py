import json
import logging
import jwt
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Solution
from jotting_jwts.settings import ACCESS_TOKEN
from django.core.cache import cache

get_url = f'https://hackattic.com/challenges/jotting_jwts/problem?access_token={ACCESS_TOKEN}'
post_url = f'https://hackattic.com/challenges/jotting_jwts/solve?access_token={ACCESS_TOKEN}'
# Get an instance of a logger
logger = logging.getLogger(__name__)


def start(request):
    if request.method == "GET":
        logger.info(f'get url {get_url}')
        get_jwt_secret = requests.get(get_url)
        jwt_secret = json.loads(get_jwt_secret.text)['jwt_secret']
        with open('key.json', 'w') as fp:
            json.dump({'key': jwt_secret}, fp)

        logger.info(f'jwt_secret {jwt_secret}')

        try:
            requests.post(post_url, data=json.dumps({'app_url': 'https://kob22hack.herokuapp.com/challenge/listener/'}), timeout = 1)
        except requests.exceptions.ReadTimeout:
            pass

        return JsonResponse({'result': 'ok'})


@csrf_exempt
def listener(request, solution=[]):
    if request.method == "POST":
        with open('key.json', 'r') as fp:
            key = json.load(fp)

        logger.info(f'listner data {request.body}')
        try:
            logger.info(f"{request.body.decode('utf-8')}  {key}")
            decoded = jwt.decode(request.body.decode('utf-8'), key['key'])
            solution_part = decoded.get('append', None)
            logger.info(f'solution part: {solution_part}')
            if solution_part:
                solution.append(solution_part)

            else:
                logger.info(f'send solution: {solution}')
                send_solution = requests.post(post_url, data=json.dumps({'solution': ''.join(solution), 'app_url': 'https://kob22hack.herokuapp.com/challenge/listener/'}))
                logger.info(f'solution response {send_solution.text}')
                solution = []

        except jwt.exceptions.InvalidTokenError:
            logger.info(f'wrong token for jwt {request.body}')

    return JsonResponse({'result': 'ok'})
