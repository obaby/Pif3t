import json

from django.http import JsonResponse
from django.shortcuts import render
from ifdata.models import *
import _thread
import requests

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from python_if_this_then_that.settings import API_KEY, API_SECRCT


def json_response_message(status, message):
    content = {
        'status': status,
        'message': message,
    }
    return JsonResponse(content)


def process_action(speech_text, if_this_object_set):
    no_action_response_text = None
    actions = None
    print('-' * 130)
    print('[P] Process Speech:')
    print('[S] Speech = ', speech_text)

    def get_action(speech, if_this_set):
        is_in_cond = False
        for it in if_this_set:
            it_key_words = it.key_words.split('|')
            for key in it_key_words:
                # 如果匹配到关键字进行自梳搜索
                if key in speech:
                    is_in_cond = True
                    print('*' * 100)
                    print('[A] Action ID=', str(it.id), ' Name= ', it.name)
                    global no_action_response_text
                    global actions
                    no_action_response_text = it.no_action_response_text
                    actions = it.that_action.all()
                    get_action(speech, it.ifthis_set.order_by('-priority', 'id'))
                    return no_action_response_text, actions
        if not is_in_cond:
            return '我还不能理解您的意图，去配置更多的规则来处理吧', None

    nrt, actx = get_action(str(speech_text).replace(' ', ''), if_this_object_set)
    print('-' * 130)
    return nrt, actx


def http_get(url, header_string):
    try:
        headers = {
            'User-Agent': 'Pif3t/v1.0.1',
        }
        try:
            headers = json.loads(header_string)
        except:
            pass
        resp = requests.get(url, timeout=5, headers=headers)
        print('[H] Http get, response=', resp.text)
        return resp.text
    except Exception as e:
        print(e)
        return None


def http_post(url, payload, header_string):
    try:
        headers = {
            'User-Agent': 'Pif3t/v1.0.1',
        }
        try:
            headers = json.loads(header_string)
        except:
            pass
        ret = requests.post(url, data=payload, timeout=5, headers=headers)
        print('[H] Http post, response=', ret.text)
        return ret.text
    except:
        return None


def deal_with_actions(actions):
    response_text = ''
    for a in actions:
        # a = ThatAction.objects.get(id=1)
        if a.http_method.lower() == 'get':
            _thread.start_new_thread(http_get, (a.http_url, a.http_header))
        elif a.http_method.lower() == 'post':
            _thread.start_new_thread(http_post, (a.http_url, a.http_body, a.http_header))
        response_text += a.response_text + '。'

    return response_text


@csrf_exempt
def speech_process(request):
    """
    http://127.0.0.1:8001/api/speech-process/?speech=你好

    post 以json方式发送参数 {"speech":"你好"}
    :param request:
    :return: 处理后的反馈语音信息
    """
    api_key = api_secret = ''
    speech = ''
    if request.method == 'GET':
        try:
            speech = request.GET['speech']
            api_key = request.GET['api_key']
            api_secret = request.GET['api_secret']
        except:
            pass
    elif request.method == 'POST':
        try:
            jd = json.loads(request.body)
            speech = jd['speech']
            api_key = jd['api_key']
            api_secret = jd['api_secret']
        except:
            speech = ''
    else:
        return json_response_message(status=2, message='错误的请求方法')

    if api_key != API_KEY or api_secret != API_SECRCT:
        return json_response_message(status=3, message='非法请求')

    speech = speech.replace(' ', '')
    if len(speech) == 0:
        return json_response_message(status=1, message='您啥都不说，我怎么知道你啥意思？')

    if_this_set = IfThis.objects.filter(parent=None).order_by('-priority', 'id')

    resp, actions = process_action(speech, if_this_set)
    print(resp)
    print(actions)
    if actions is None or len(actions) == 0:
        return json_response_message(status=0, message=resp)
    resp = deal_with_actions(actions)

    return json_response_message(status=0, message=resp)


def home_page(request):
    variables = {
        "username": request.user.username,
        'page_name': '',
    }
    return render(request, 'home_page/index.html', variables)
