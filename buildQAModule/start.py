import flask
import json
from flask import request
from chat_robot import ChatBotGraph

# flask： web框架，通过flask提供的装饰器@server.route()将普通函数转换为服务
# 问答模块，接收自然问句，返回自然答案

# 创建一个服务，把当前这个python文件当做一个服务
app = flask.Flask(__name__)


# @server.route()可以将普通函数转变为服务 登录接口的路径、请求方式
@app.route('/chat_robot', methods=['get', 'post'])
def chat_robot():
    # 获取自然问句l
    question = request.values.get('question')
    # 判断问句不为空
    if question:
        handler = ChatBotGraph()
        answer = handler.chat_main(question)
        return json.dumps(answer, ensure_ascii=False)
    else:
        result = {'result': False, 'message': '问句不能为空！'}
        return json.dumps(result, ensure_ascii=False)


if __name__ == '__main__':
    # 指定端口、host,0.0.0.0代表不管几个网卡，任何ip都可以访问
    app.run(port=8088, host='0.0.0.0')
