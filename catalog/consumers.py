import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # Имя комнаты (в каком нить реальном проекте можно брать из URL)
        self.room_group_name = "pinkstore_chat"


        # подписываем текущее соединение на группу
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )


        self.accept()
        
        # проверяем пользователя (он подтянется автоматически благодаря AuthMiddlewareStack)
        user = self.scope.get("user")
        name = user.username if user and user.is_authenticated else "Аноним"


        self.send(text_data=json.dumps({
            "message": f"Привет, {name}! Вы в чатике!)"
        }))


    def disconnect(self, close_code):
        # отписываемся от группы при отключении
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name,
        )


    def receive(self, text_data=None, bytes_data=None):
        if text_data is None:
            return


        data = json.loads(text_data)
        message = data.get("message", "")
        
        user = self.scope.get("user")
        name = user.username if user and user.is_authenticated else "Анонимус"


        # отправляем сообщение ВО ВСЮ ГРУППУ
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",  # какую функцию вызвать у потребителей
                "message": f"{name}: {message}",
            },
        )


    def chat_message(self, event):
        # эта функция вызывается у ВСЕХ участников группы, когда мы делаем group_send
        message = event["message"]


        self.send(text_data=json.dumps({
            "message": message
        }))
