import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextSendMessage, MessageEvent, TextMessage

# 建立 Flask 應用
app = Flask(__name__)

# 設定 Line Bot API 和 WebhookHandler
bot_api = LineBotApi('ibxVmiLsI9lWbS+R+wr+wQcZIZu73+bHlr8jn4edebUYYYB57IWPgrUpwcvCKf0HGzgsDg7JE0JbZVdQBAxEe6NW10Nob5zmrtgqCGzHfiqy/2Cp1QHKnPclN2kWYywmR7LmGLLQx4QrOxdTMJaRLgdB04t89/1O/w1cDnyilFU=')  # 這裡填入你的 Channel Access Token
bot_handler = WebhookHandler('46050724507c695901b944404aa4fda3')  # 這裡填入你的 Channel Secret

# 啟動時發送訊息通知
bot_api.push_message('U6688362b6a234c9f16a095b8b91a8cae', TextSendMessage(text='啟動!!!!!!'))

# 定義一個路由來處理 /feedback 的請求
@app.route("/feedback", methods=['POST'])
def handle_request():
    signature_header = request.headers['X-Line-Signature']
    request_body = request.get_data(as_text=True)
    app.logger.info("Received body: " + request_body)

    try:
        bot_handler.handle(request_body, signature_header)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 處理訊息事件的函數
@bot_handler.add(MessageEvent, message=TextMessage)
def respond_to_message(event):
    response_message = TextSendMessage(text=event.message.text)
    bot_api.reply_message(event.reply_token, response_message)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)