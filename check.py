import json
import random

import requests


def request_http(url, post=False, post_data=''):
    data = {}
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/90.0.4430.93 Safari/537.36',
    }

    if 'snapchat' in url:
        headers['cookie'] = 'xsrf_token=1'
        headers['content-type'] = 'application/x-www-form-urlencoded; charset=utf-8'

    if get_available_proxies():
        proxy = random.choice(get_available_proxies())
        proxies = {
            "http": "https://" + proxy,
            "https": "https://" + proxy,
        }
        try:
            if post:
                r = requests.post(url, allow_redirects=True, headers=headers, proxies=proxies, data=post_data)
            else:
                r = requests.get(url, allow_redirects=True, headers=headers, proxies=proxies)
            if 'snapchat' in url:
                if 'TAKEN' in str(r.content):
                    data['http_code'] = 200
                else:
                    data['http_code'] = 404
            else:
                data['http_code'] = r.status_code
                data['response'] = r.content
            return data
        except requests.ConnectionError:
            return -1
    else:
        try:
            if post:
                r = requests.post(url, allow_redirects=True, headers=headers,
                                  data=post_data)
            else:
                r = requests.get(url, allow_redirects=True, headers=headers)

            if 'snapchat' in url:
                if 'TAKEN' in str(r.content):
                    data['http_code'] = 200
                else:
                    data['http_code'] = 404
            else:
                data['http_code'] = r.status_code
                data['response'] = r.content
            return data
        except requests.ConnectionError:
            return -1


def get_available_websites():
    string = []
    with open('settings.json') as available_file:
        for sites in json.load(available_file)['custom_sites']:
            string.append(sites + ", ")
    return (''.join(string))[:-2]


def get_available_proxies():
    with open('settings.json') as available_file:
        return json.load(available_file)['proxies']


print(r"""
   ___   ____ _   _   ______ _____  __
  / _ \ / ___| | | | / / ___|_ _\ \/ /
 | | | | |  _| | | |/ /\___ \| | \  / 
 | |_| | |_| | |_| / /  ___) | | /  \ 
  \___/ \____|\___/_/  |____/___/_/\_\
  OGCheckr - v0.1                 @six
                """)

filename = input('- Filename with usernames (e.g. usernames.txt): ')
if not filename:
    filename = 'usernames.txt'

print("- Available sites: " + get_available_websites())

with open(filename, 'r') as file:
    for line in file:
        with open('settings.json') as json_file:
            custom_sites = json.load(json_file)['custom_sites']
            total_sites = len(custom_sites.values())
            available = 0
            for idx, site in enumerate(custom_sites.values()):

                if list(custom_sites.keys())[idx] == 'snapchat':
                    request = request_http(site, post=True,
                                           post_data='requested_username=' + line.strip() + '&xsrf_token=1')
                    http_code = request['http_code']
                else:
                    request = request_http(site % line.strip())
                    http_code = request['http_code']
                    response = request['response']

                if list(custom_sites.keys())[idx] == 'twitter':
                    if json.loads(response)['valid']:
                        available = available + 1
                        f = open("available/" + list(custom_sites.keys())[idx] + ".txt", 'a')
                        f.write(line.strip() + '\r\n')
                        f.close()
                else:
                    if http_code == 404 or http_code == 204:
                        available = available + 1
                        f = open("available/" + list(custom_sites.keys())[idx] + ".txt", 'a')
                        f.write(line.strip() + '\r\n')
                        f.close()
            print('@' + line.strip() + ' available [' + str(available) + '/' + str(total_sites) + ']')
    print("- All finished! Please check your available/ folder")
