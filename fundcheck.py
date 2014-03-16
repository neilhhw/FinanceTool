#!/usr/bin/env python
# -*- coding: utf-8 -*-

import httplib, urllib, re

PROXY = ""
PORT = 80
UTF_CHINESE = "[\u0391-\uFFE5]*"
GBK_CHINESE = "[\x00-\xff]+"
URL = "fund.eastmoney.com"

conn = None

def establish():
    """establish connection"""
    global conn
    if PROXY != "":
        conn = httplib.HTTPConnection(PROXY, PORT)
    else:
        conn = httplib.HTTPConnection(URL, PORT)

def get_fund_value(fund_num):
    """get fund value from fund number"""
    if PROXY != "":
        url = "http://fund.eastmoney.com/%s.html" % fund_num
    else:
        url = "/%s.html" % fund_num

    conn.request("GET", url)
    resp = conn.getresponse()
    data = resp.read()
    parse(data, fund_num)

def parse(data, num):
    """parse html data to readable value"""
    info_re = "<div class=\"fund_info\">.*</div>"
    matches = re.findall(info_re, data)
    for m in matches:
        est_re = "<div id=\"statuspzgz\".*<div id=\"btncanbuy\""
        est = re.findall(est_re, m)
        value = "<span class=\"\w*\s\w*\">(\d*\.\d*)</span>"
        val_list = re.findall(value, est[0])
        ran = "class=\"\w*\s*\w*\">(-?\d*\.\d*%)"
        ran_list = re.findall(ran, est[0])

        name_re = "<a href=\"%d.html\"\s*>(%s)</a><span" % (num, GBK_CHINESE)
        names = re.findall(name_re, m)

        #print m
        result = {'estimation': val_list[0], 'value': val_list[1],
                'estimation range': ran_list[0], 'range': ran_list[1], 'name': names[0].decode('gbk').encode('utf-8')}
        print_data(result)

def print_data(result):
    """print data to screen"""
    print "============================================================================"

    print "%s\t%s\t%s\t%s\t%s" % (result['name'], result['value'], result['range'], result['estimation'], result['estimation range'])

    '''
    for k, v in result.items():
        print k, v
    '''

def set_proxy(server, port, **kargs):
    """set proxy"""
    global PROXY, PORT
    PROXY = server
    PORT = port

#set_proxy("10.144.1.10", 8080)
establish()

print "Name\tValue\tRange\tEstimation\tEstimation Range"
get_fund_value(110023)
get_fund_value(110029)
