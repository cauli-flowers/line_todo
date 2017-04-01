from flask import Flask, jsonify, make_response, request
from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError
from database import create_table
import configparser
import peewee

config = configparser.ConfigParser()
config.read('./config.ini')

ACCESS_TOKEN = config.get('line', 'access_token')
USER_ID = config.get('line', 'user_id')

create_table()

db = peewee.PostgresqlDatabase(
    config.get('postgres', 'database'),
    user=config.get('postgres', 'user'),
    password=config.get('postgres', 'password'),
    host=config.get('postgres', 'host'),
)


class Todo(peewee.Model):
    id = peewee.PrimaryKeyField()
    title = peewee.CharField()
    details = peewee.TextField()
    done = peewee.BooleanField()
    limit = peewee.DateTimeField()
    notification = peewee.DateTimeField()

    class Meta:
        database = db

api = Flask(__name__)

line_bot_api = LineBotApi(ACCESS_TOKEN)


@api.route('/', methods=['GET'])
def hello_world():
    return 'hello world'


@api.route('/todo', methods=['GET'])
def get_todo():
    try:
        todos = Todo.select().where(Todo.done == False)

        result = []

        for todo in todos:
            item = {
                'title': todo.title,
                'details': todo.details,
                'done': todo.done,
                'limit': todo.limit,
                'notification': todo.notification,
            }
            result.append(item)

    except Todo.DoesNotExist:
        result = []

    return make_response(jsonify(result))


@api.route('/todo/<string:todo_id>/message', methods=['POST'])
def push_message(todo_id):
    todo_id = todo_id
    message = request.form['message']
    try:
        line_bot_api.push_message(USER_ID, TextSendMessage(text=message))
        return message
    except LineBotApiError as e:
        print(e)
        return message


@api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    api.run(host='0.0.0.0', port=3000)