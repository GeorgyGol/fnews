import requests

def send_message2(strText):
    strAPI = fr'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={channel_id}&text={strText}&parse_mode=html'
    res = requests.get(strAPI)
    return res.status_code

if __name__ == '__main__':
    # executor.start_polling(dp, skip_updates=True, on_startup=test)
    # executor.start(dp, test())
    # send_message('test')
    print('all done')
