#author by Arice
import argparse
import requests
import time
import re
from io import StringIO
from concurrent.futures import ThreadPoolExecutor

def para_options():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u",help = "input your domain or ip,need add http:// https://")
    parser.add_argument("-t", type = int ,help = "input your Thread,default is 5")
    parser.add_argument("-d",help = "input your dict,default is common.txt")
    args = parser.parse_args()
    return args

def file_dict(parameter_name):
    filename = []
    if parameter_name == None:
        filedict = open("./dict/common.txt")
        for line in filedict.readlines():
            filename.append(line.strip())
        filedict.close()
    else:
        parameter_name = parameter_name.split(',')
        print(parameter_name)
        for l in parameter_name:
            filedict = open('./dict/'+l + ".txt")
            for line in filedict.readlines():
                filename.append(line.strip())
            filedict.close()
    return filename

def num_molecular():
    n = f.getvalue()
    if n == '':
        f.write(str(1))
    else:
        n = int(n) + 1
        f.truncate()
        f.seek(0)
        f.write(str(n))
    return f.getvalue()
def num_grave():
    l = 0
    if para_options().d == None:
        l = len([ "" for line in open("./dict/common.txt","r")])
    else:
        for para in para_options().d.split(','):
            l = l +len([ "" for line in open("./dict/"+para+".txt","r")])
    return l

def head(fname):
    url = para_options().u + fname
    molecular = int(num_molecular())
    headers = {
"User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
}
    re_key = re.compile('<title>(.*?)</title>',re.S)
    try:
        s = requests.head(url, headers = headers, timeout = 2)
        r = requests.get(url, headers = headers, timeout = 2)
        if s.status_code == 200:
            num = 0
            if r.text not in compare_text:
                if len(compare_text) <10:
                    compare_text.append(r.text)   
                r.encoding = 'utf-8'
                Val = re.findall(re_key,r.text)
                for title in key_title:
                    if title in "".join(Val):
                        num += 1
                        #print("".join(Val))
                    else:
                        pass
                r.encoding = 'gbk'
                Val = re.findall(re_key,r.text)
                for title in key_title:
                    if title in "".join(Val):
                        num += 1
                        #print("".join(Val))
                    else:
                        pass
                if num < 1:
                    print('\033[1;32m{} \033[0m------状态码:{}------\033[1;35m 完成度为:{:.2%} \033[0m'.format(r.url,r.status_code,molecular/int(num_grave())))
        elif s.status_code == 302:
            num = 0
            #print(s.status_code)
            if r.url not in compare:
                if len(compare) < 1000:
                    compare.append(s.url)
                r.encoding = 'utf-8'
                Val = re.findall(re_key,r.text)
                for title in key_title:
                    if title in "".join(Val):
                        num += 1
                    else:
                        pass
                r.encoding = 'gbk'
                Val = re.findall(re_key,r.text)
                for title in key_title:
                    if title in "".join(Val):
                        num += 1
                    else:
                        pass
                if num < 1:
                    print('\033[1;33m{} \033[0m-----302跳转,状态:{}------\033[1;35m 完成度为:{:.2%} \033[0m'.format(r.url,r.status_code,molecular/int(num_grave())))
        elif s.status_code == 403:
            num = 0
            print('\033[1;34m{} \033[0m------状态码:{}------\033[1;35m 完成度为:{:.2%} \033[0m'.format(s.url,s.status_code,molecular/int(num_grave())))
            
    except requests.exceptions.ConnectTimeout:
        NETWORK_STATUS = False
    except requests.exceptions.Timeout:
        REQUEST_TIMEOUT = True

def bing():
    keys = ['','admin','login','action','do']
    domain = para_options().u.lstrip('https://').lstrip('http://')
    if ':' in domain:
        domain = domain[0:domain.index(':')]
    elif '/' in domain:
        domain = domain[0:domain.index('/')]
    else:
        pass
    headers = {
"User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
}
    for key in keys:
        if re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$',domain):
            url = 'https://www.bing.com/search?q=ip:'+domain+'+'+key
        else:
            url = 'https://www.bing.com/search?q=site:'+domain+'+'+key
        req = requests.get(url,headers = headers)
        patt = re.compile('<li class="b_algo"><h2><a target="_blank" href="(.*?)" h=".*?">(.*?)</a></h2>')
        Values = re.findall(patt,req.text)
        for V in Values:
            site = str(V[0])
            print('\033[1;36m{} \033[0m----{}'.format(site,V[1]))


def Thread_main(filename):
    if para_options().t == None:
        with ThreadPoolExecutor(10) as executor:
            executor.map(head, filename)
    else:
        with ThreadPoolExecutor(para_options().t) as executor:
            executor.map(head, filename)



if __name__ == '__main__':
    key_title = ['抱歉', '对不起','页面','存在','不','sorry','404', 'error']
    compare = [para_options().u]
    exp = para_options().u + '/zzzzzzzztest'
    #t = requests.get(exp, headers = headers, timeout = 2).text
    compare_text = [requests.get(exp, timeout = 2).text]
    #print(compare_text)
    n = 0
    f = StringIO()
    if para_options().u:
        bing()
        Thread_main(file_dict(para_options().d))