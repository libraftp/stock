from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextSendMessage, MessageEvent, TextMessage
import os

app = Flask(__name__)

# 設定 Line Bot API 和 WebhookHandler
bot_api = LineBotApi('ibxVmiLsI9lWbS+R+wr+wQcZIZu73+bHlr8jn4edebUYYYB57IWPgrUpwcvCKf0HGzgsDg7JE0JbZVdQBAxEe6NW10Nob5zmrtgqCGzHfiqy/2Cp1QHKnPclN2kWYywmR7LmGLLQx4QrOxdTMJaRLgdB04t89/1O/w1cDnyilFU=')
bot_handler = WebhookHandler('46050724507c695901b944404aa4fda3')

@app.route('/')
def home():
    app.logger.info("Home route was accessed")
    print("Home route was accessed")
    return 'Welcome to the Flask app!'

# 發送初始消息，確認推送功能正常
bot_api.push_message('U6688362b6a234c9f16a095b8b91a8cae', TextSendMessage(text='你可以開始了'))

@app.route("/feedback", methods=['POST'])
def handle_request():
    app.logger.info("Feedback route was accessed")
    print("Feedback route was accessed")

    signature_header = request.headers.get('X-Line-Signature')
    request_body = request.get_data(as_text=True)
    
    # 打印請求信息
    app.logger.info(f"Received body: {request_body}")
    app.logger.info(f"Signature header: {signature_header}")
    print(f"Received body: {request_body}")
    print(f"Signature header: {signature_header}")

    try:
        bot_handler.handle(request_body, signature_header)
        app.logger.info("Handle successful")
        print("Handle successful")
        return 'success'
    except InvalidSignatureError:
        app.logger.error("Invalid signature. Aborting request.")
        print("Invalid signature. Aborting request.")
        abort(400)

    return 'OK'

@bot_handler.add(MessageEvent, message=TextMessage)
def respond_to_message(event):
    app.logger.info(f"Received message: {event.message.text}")
    print(f"Received message: {event.message.text}")

    response_message = TextSendMessage(text=event.message.text)
    bot_api.reply_message(event.reply_token, response_message)
    
    app.logger.info("Message responded successfully")
    print("Message responded successfully")

    return 'OK'
if __name__ == "__main__":
    port_number = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port_number)
