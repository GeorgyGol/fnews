import unittest
from unittest import TestCase
from app import app as tested_app
from app import views, rss, telega
import json
import datetime as dt
import re
from pathlib import Path
from os import getcwd

class TestNewsAdm(TestCase):
    def setUp(self):
        tested_app.config['TESTING'] = True
        self.app = tested_app.test_client()

    def test_index(self):
        r = self.app.get('/')
        return self.assertEqual(r.status_code, 200)

    def test_data(self):
        r = self.app.get('/api/data')
        self.assertGreater(len(r.json['data']), 10)

    def test_rss(self):
        if re.search('/app$', getcwd()) is not None:
            strAdd = ''
        else:
            strAdd = 'app'

        try:
            rss.update_rss(nnum='TEST', ndate=dt.datetime.now(),
                           ntext='for testing only', ntitle='UNITTEST',
                           file_path=str(Path(strAdd, 'rss', 'rss.xml')))
            rss.delete_item(guid='TEST', file_path=str(Path(strAdd, 'rss', 'rss.xml')))
            self.assertTrue(True)
        except:
            self.assertTrue(False, msg='Some errors for RSS-work')

    def test_telega_mess(self):
        strText = '''If you see this page, 
            the nginx web server is successfully<br> 
            installed and working. Further configuration is required.<BR /><br>
        <Br>
        For online documentation and support please refer to nginx.org.
        Commercial support is available at nginx.com.'''

        cor_mess = telega.correct_mess(strText)
        t1 = re.search('(?im)<br\s?/?>', cor_mess) is None
        self.assertTrue(t1)


if __name__ == '__main__':
    unittest.main()