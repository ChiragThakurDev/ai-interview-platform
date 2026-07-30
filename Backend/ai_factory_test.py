from app.ai.factory import AIFactory

chat1 = AIFactory.chat()
chat2 = AIFactory.chat()

print(chat1 is chat2)
