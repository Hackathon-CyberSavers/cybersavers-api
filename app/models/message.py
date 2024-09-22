from .. import mongo
from datetime import datetime, timedelta

class Message:
    def __init__(self, message, role, user_id):
        self.message = message,
        self.role = role,
        self.user_id = user_id,
        self.created_at = datetime.now()

    @staticmethod
    def from_dict(data):
        return Message(
            message=data.get("message"),
            role=data.get("role"),
            user_id=data.get("user_id"),
            created_at=data.get("created_at"),
        )
    
    def to_dict(self):
        return {
            "message": self.message,
            "role": self.role,
            "user_id": self.user_id,
            "created_at": self.created_at, 
        }
    
    @staticmethod
    def get_all_chat_by_user_id(user_id):
        thirty_minutes_ago = datetime.now() - timedelta(minutes=30)
        cursor = mongo.db.messages.find(
            {"user_id": user_id, "created_at": {"$gte": thirty_minutes_ago}},
            {"_id": 0, "user_id": 0}
        ).sort("created_at", 1)

        messages = list(cursor)
        return messages
    
    @staticmethod
    def create_message(message_data):
        return mongo.db.messages.insert_one(message_data)
    
    @staticmethod
    def delete_chat_by_user_id(user_id):
        return mongo.db.messages.delete_many({"user_id": user_id})

