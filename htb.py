#!/usr/bin/python3

import codecs
import base64
import requests


base_url = 'https://www.hackthebox.eu'

def getInviteCode():
    """
    https://www.hackthebox.eu/js/inviteapi.min.js
    eval(function(p,a,c,k,e,d){e=function(c){return c.toString(36)};if(!''.replace(/^/,String)){while(c--){d[c.toString(a)]=k[c]||c.toString(a)}k=[function(e){return d[e]}];e=function(){return'\\w+'};c=1};while(c--){if(k[c]){p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c])}}return p}('1 i(4){h 8={"4":4};$.9({a:"7",5:"6",g:8,b:\'/d/e/n\',c:1(0){3.2(0)},f:1(0){3.2(0)}})}1 j(){$.9({a:"7",5:"6",b:\'/d/e/k/l/m\',c:1(0){3.2(0)},f:1(0){3.2(0)}})}',24,24,'response|function|log|console|code|dataType|json|POST|formData|ajax|type|url|success|api|invite|error|data|var|verifyInviteCode|makeInviteCode|how|to|generate|verify'.split('|'),0,{}))

    deobfuscated:
    function makeInviteCode() {
      $.ajax({
        type : "POST",
        dataType : "json",
        url : "/api/invite/how/to/generate",
        success : function(response) {
          console.log(response);
        },
        error : function(response) {
          console.log(response);
        }
      });
    """
    r = requests.request('POST',f'{base_url}/api/invite/how/to/generate', data={})
    r.raise_for_status()
    # print(r.json())
    enc_type = r.json()['data']['enctype']
    if enc_type == 'BASE64':
        msg = base64.b64decode(r.json()['data']['data']).decode()  # In order to generate the invite code, make a POST request to /api/invite/generate
    else:  # only ever else seen rot13
        msg = codecs.encode(r.json()['data']['data'], 'rot_13')
    # print(msg)
    endpoint = msg.split()[-1]
    r = requests.request('POST',f'{base_url}{endpoint}', data={})
    r.raise_for_status()
    code = base64.b64decode(r.json()['data']['code']).decode()

    return code

def register(username, email, password, invite_code=None, captcha_token=None):
    # todo resolve captcha token - integrate token harvester? data-sitekey=6Ldh_h0UAAAAAD74rB9uzS7sAmyt-GhkVSMFlwt3
    if invite_code is None:
        invite_code = getInviteCode()
    token = ''  # scraped from form page 
    payload = {
        '_token': token,
        'code': code,
        'name': username,
        'email': email,
        'password': password,
        'accept_tos': 'on',
        'g-recaptcha-response': captcha_token
    }
    r = requests.request('POST',f'{base_url}/register', data=payload)

print(getInviteCode())

