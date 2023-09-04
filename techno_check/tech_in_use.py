# import six
# import sys
import os
import re
import json
import requests
from datetime import datetime

def builtwith(url, request_obj, headers=None, html=None):
    techs = {}

    # check URL
    for app_name, app_spec in data['apps'].items():
        if 'url' in app_spec:
            if contains(url, app_spec['url']):
                add_app(techs, app_name, app_spec)

    if None in (headers, html):
        try:
            response =  request_obj #requests.get(url, headers=headers)
            html = response.text

        except requests.exceptions.RequestException as e:
            print('Error:', e)


    # check headers
    if headers:
        for app_name, app_spec in data['apps'].items():
            if 'headers' in app_spec:
                if contains_dict(headers, app_spec['headers']):
                    add_app(techs, app_name, app_spec)
 

    # check html
    import time
    s_time = time.time()
    if html:

        loop_count = 1
        for app_name, app_spec in data['apps'].items():
            e_time  = time.time()
            for key in 'html', 'script':
                loop_count = loop_count + 1
                snippets = app_spec.get(key, [])
        
                if not isinstance(snippets, list): 
                    snippets = [snippets]
                   
                for snippet in snippets:

                    if contains(html, snippet): 
                        add_app(techs, app_name, app_spec)
                        break
            
            if loop_count < 100 and round(e_time - s_time) == 1:
                print('issue with the website')
                break
    
            # print('out of in loop $$$$$$$$$$$$$$$$$$$')


        # check meta
        #  add proper meta data parsing
 
        # if six.PY3 and isinstance(html, bytes):
        if isinstance(html, bytes):
            
            html = html.decode()
        metas = dict(re.compile('<meta[^>]*?name=[\'"]([^>]*?)[\'"][^>]*?content=[\'"]([^>]*?)[\'"][^>]*?>', re.IGNORECASE).findall(html))
        for app_name, app_spec in data['apps'].items():
            

            for name, content in app_spec.get('meta', {}).items():
                if name in metas:
                    if contains(metas[name], content):
                        add_app(techs, app_name, app_spec)
                        break
                
    return techs


parse = builtwith


def add_app(techs, app_name, app_spec):
    """Add this app to technology
    """
    for category in get_categories(app_spec):
        if category not in techs:
            techs[category] = []
        if app_name not in techs[category]:
            techs[category].append(app_name)
            implies = app_spec.get('implies', [])
            if not isinstance(implies, list):
                implies = [implies]
            for app_name in implies:
                add_app(techs, app_name, data['apps'][app_name])
           

def get_categories(app_spec):
    """Return category names for this app_spec
    """
    return [data['categories'][str(c_id)] for c_id in app_spec['cats']]


def contains(v, regex):
    """Removes meta data from regex then checks for a regex match
    """
    # if six.PY3 and isinstance(v, bytes):
    if isinstance(v, bytes):
        v = v.decode()
    return re.compile(regex.split('\\;')[0], flags=re.IGNORECASE).search(v)


def contains_dict(d1, d2):
    """Takes 2 dictionaries
    
    Returns True if d1 contains all items in d2"""
    for k2, v2 in d2.items():
        v1 = d1.get(k2)
        if v1:
            if not contains(v1, v2):
                return False
        else:
            return False
    return True


def load_apps():
    """Load apps from Wappalyzer JSON (https://github.com/ElbertF/Wappalyzer)
    """
    # get the path of this filename relative to the current script
    # XXX add support to download update
    filename =  'techno_check/apps.json.py' #os.path.join(os.getcwd(), os.path.dirname(__file__), filename)
    return json.load(open(filename))
data = load_apps()


# if __name__ == '__main__':
#     urls = sys.argv[1:]
#     if urls:
#         for url in urls:
#             results = builtwith(url)
#             for result in sorted(results.items()):
#                 print('%s: %s' % result)
#     else:
#         print('Usage: %s url1 [url2 url3 ...]' % sys.argv[0])
