from .. import mongo
from datetime import datetime

class Message:
    def __init__(self, message, role, user_id):
        self.message = message,
        self.role = role,
        self.user_id = user_id,
        self.created_at = datetime.now()
    
    # Função para criar uma instância da classe User
    @staticmethod
    def from_dict(data):
        return Message(
            message=data.get("message"),
            role=data.get("role"),
            user_id=data.get("user_id"),
            created_at=data.get("created_at"),
        )
    
    # Função para transformar o objeto User em um dicionário
    def to_dict(self):
        return {
            "message": self.message,
            "role": self.role,
            "user_id": self.user_id,
            "created_at": self.created_at, 
        }
    
    @staticmethod
    def get_all_chat_by_user_id(user_id):
        return mongo.db.messages.find({"user_id": user_id}, {"_id": 0, "created_at": 0}).sort({"created_at": 1})
    
    @staticmethod
    def create_message(message_data):
        return mongo.db.messages.insert_one(message_data)
    
    @staticmethod
    def delete_message(user_id):
        return mongo.db.messages.delete_many({"user_id": user_id})

