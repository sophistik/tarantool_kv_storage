from django.http import JsonResponse, HttpResponse
import json
import logging
from django.views.decorators.csrf import csrf_exempt
from tarantool import Connection


def valid_body(method, body):
    try:
        json_object = json.loads(body)
    except ValueError as e:
        return False
    if method == 'PUT':
        return 'value' in json_object and len(json_object) == 1
    return 'key' in json_object and 'value' in json_object and len(json_object) == 2


def get_value_by_key(key):
    c = Connection('127.0.0.1', 3301)
    value = list(c.select("KVStorage", key))
    return value


def add_value_by_key(key, value):
    c = Connection('127.0.0.1', 3301)
    c.insert("KVStorage", (key, value))
    return


def update_value_by_key(key, value):
    c = Connection('127.0.0.1', 3301)
    c.update("KVStorage", key, [('=', 1, str(value))])
    return


def delete_value_by_key(key):
    c = Connection('127.0.0.1', 3301)
    c.delete("KVStorage", key)
    return


@csrf_exempt
def post(request):
    logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s',
                                 level=logging.INFO, filename=u'logfile.log')
    body = request.body
    method = request.method

    if method != 'POST':
        return
    logging.info(u'POST')
    if not valid_body(method, body):
        logging.warning(u'400 Body is not correct')
        return JsonResponse({'error': 'Body is not correct.'}, status=400)

    d = json.loads(body)
    key = str(d['key'])
    value = str(d['value'])

    if get_value_by_key(key):
        logging.warning(u'409 Key exists')
        return JsonResponse({'error': 'Key exists'}, status=409)
    add_value_by_key(key, value)

    logging.info(u'200 OK')
    return HttpResponse(status=200)


@csrf_exempt
def another(request, id):
    logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s',
                                 level=logging.INFO, filename=u'logfile.log')
    key = str(id)
    body = request.body
    method = request.method

    if method == 'PUT':
        logging.info(u'PUT')
        if not valid_body(method, body):
            logging.warning(u'400 Body is not correct')
            return JsonResponse({'error': 'Body is not correct.'}, status=400)
        if not get_value_by_key(key):
            logging.warning(u'404 Not found')
            return JsonResponse({'error': 'Key doesnt exists.'}, status=404)
        d = json.loads(body)
        value = d['value']
        update_value_by_key(key, value)
        return HttpResponse(status=200)

    elif method == 'GET':
        logging.info(u'GET')
        response = get_value_by_key(key)
        if not response:
            logging.warning(u'404 Not found')
            return JsonResponse({'error': 'Key doesnt exists.'}, status=404)

        jsn = json.dumps(response[0][-1])
        return HttpResponse(jsn)

    elif method == 'DELETE':
        logging.info(u'DELETE')
        if not get_value_by_key(key):
            logging.warning(u'404 Not found')
            return JsonResponse({'error': 'Key doesnt exists.'}, status=404)
        delete_value_by_key(key)
        return HttpResponse('OK')

