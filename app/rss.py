import xml.etree.ElementTree as ET

import  requests
import datetime as dt
from pathlib import Path
import os

strItemTemplate = '''
<item>
        <title>{news_title}</title>
        <link>http://www.forecast.ru/default.aspx</link>
        <description>{news_text}</description>
        <autor>CMASF</autor>
        <pubDate>{news_date}</pubDate>
        <guid>{news_num}</guid>
        <category>macroeconomica</category>
    </item>
'''

def update_rss(ndate = None, nnum=None, ntext='', ntitle = 'Обновление сайта ЦМАКП', file_path='rss.xml'):
    assert type(ndate) == dt.datetime
    assert nnum is not None
    assert len(ntext)>0

    newtext = ntext.replace('<', '&lt;').replace('>', '&gt;')

    if Path(file_path).exists():
        tree = ET.parse(file_path)
        root = tree.getroot()
    else:
        response = requests.get('http://www.forecast.ru/feed/rss.xml')
        root = ET.fromstring(response.content)
        tree = ET.ElementTree(root)

    for item in root[0].findall('item'):
        try:
            if int(item.find('guid').text) == nnum:

                item.find('description').text = newtext
                item.find('pubDate').text = ndate.strftime('%a, %d %b %Y %H:%M:%S %Z')
                tree.write(file_path, encoding="utf-8")

                return
        except:
            pass

    xnew = ET.fromstring(strItemTemplate.format(news_title=ntitle,
                                                news_text=newtext,
                                                news_date=ndate.strftime('%a, %d %b %Y %H:%M:%S %Z'),
                                                news_num=nnum))
    xnew.tail='\n\t'

    root[0].insert(11, xnew)
    try:
        ET.indent(tree, space="\t", level=0)
    except AttributeError:
        pass # запуск из Питона младших версий
    tree.write(file_path, encoding="utf-8")

def delete_item(guid=0, file_path = 'rss.xml'):
    assert Path(file_path).exists()
    tree = ET.parse(file_path)
    root = tree.getroot()

    for item in root[0].findall('item'):

        try:
            if int(item.find('guid').text) == int(guid):
                root[0].remove(item)
                ET.indent(tree, space="\t", level=0)
                tree.write(file_path, encoding="utf-8")
                return int(guid)
        except:
            root[0].remove(item)

    ET.indent(tree, space="\t", level=0)
    tree.write(file_path, encoding="utf-8")


if __name__ == '__main__':
    # dtn = dt.datetime.now()
    # print(dtn.strftime('%a, %d %b %Y %H:%M:%S %Z'))
    # update_rss(ndate=dtn, nnum=10, ntext='chao-chao')
    #
    # tree = ET.parse('rss.xml')
    # ET.dump(tree)
    print('Add done')
    # delete_item(guid=10)