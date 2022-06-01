import requests
from app import bot_token, channel_id
import re

def send_message2(strText):
    mess = re.sub('(?im)<br>', '', strText)
    strAPI = fr'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={channel_id}&text={mess}&parse_mode=html'
    res = requests.get(strAPI)
    return res.status_code

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

    mess = re.sub('(?im)<br>', '', strText)
    print(mess)
    print('all done')
