from bs4 import BeautifulSoup
import argparse
import os
import requests
from requests_html import HTMLSession
import urllib
import sys
import ast
import json

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-q', '--query', default='青椒肉絲', type=str, help='検索クエリ', required=True)
    parser.add_argument('-n', '--num', default=10, type=int, help='獲得してくる画像の枚数', required=True)
    parser.add_argument('-o', '--out_dir', type=str, default='data/tmp', help='出力ディレクトリ', required=True)
    args = parser.parse_args()
    return args

def makeOutDir( outdir ):
    if not os.path.exists( outdir ):
        os.makedirs( outdir )

def get_userAgent():
    session = HTMLSession()
    ua = session.get('http://httpbin.org/user-agent')
    return ast.literal_eval( ''.join( ua.text.split() ) )

def get_soup( url, headers ):
    return BeautifulSoup(requests.get(url,headers=headers).content, 'lxml')

def crawlImage( query, num, outdir ):
    url = "https://www.google.co.jp/search?q="+query+"&source=lnms&tbm=isch"
    headers = get_userAgent()
    soup = get_soup( url,headers )

    for i, s in enumerate(soup.find_all("div",{"class":"rg_meta"}, limit=num)):
        link = json.loads(s.text)['ou']
        try:
            img = urllib.request.urlopen( link ).read()
            with open( os.path.join(outdir, 'img_'+str(i)+'.jpg'), 'wb' ) as f:
                f.write(img)
        except:
            pass

def main():
    args = get_args()
    query = args.query
    num = args.num
    outdir = args.out_dir

    makeOutDir( outdir )
    crawlImage( query, num, outdir )

if __name__=='__main__':
    main()


