import requests
from app import bot_token, channel_id
import re

def correct_mess(strMess):
    mess = re.sub('(?im)<br\s?/?>', '', strMess)
    return mess

def send_message2(strText, do_post=True):
    assert len(bot_token) > 10
    assert len(channel_id) > 5
    mess = correct_mess(strText)
    if do_post:
       strAPI = fr'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={channel_id}&text={mess}&parse_mode=html'
       res = requests.get(strAPI)
       return res.status_code
    else:
       return -1

if __name__ == '__main__':
    # executor.start_polling(dp, skip_updates=True, on_startup=test)
    # executor.start(dp, test())
    # send_message2('test')
    strText = '''If you see this page, 
    the nginx web server is successfully<br> 
    installed and working. Further configuration is required.<BR><br>
<Br>
For online documentation and support please refer to nginx.org.
Commercial support is available at nginx.com.'''

    mess = correct_mess(strText)
    print(mess)
    print('all done')
