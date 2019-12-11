from threading import Thread
from app import create_app
from app import wechat

if __name__ == '__main__':
    app = create_app()
    start_info = wechat.bot.load_login_status(wechat.dir_path + '/itchat.pkl')
    if start_info:
        thread = Thread(target=wechat.wechat_main, daemon=True, args=(start_info,))
        thread.start()

    app.run(host="0.0.0.0")
