from .. import mongo

class User:
    def __init__(self, name, last_name, email, password):
        self.name = name
        self.last_name = last_name
        self.email = email
        self.password = password
    
    # Função para criar uma instância da classe User
    @staticmethod
    def from_dict(data):
        return User(
            name=data.get("name"),
            last_name=data.get("last_name"),
            email=data.get("email"),
            password=data.get("password")
        )
    
    # Função para transformar o objeto User em um dicionário
    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "last_name": self.last_name,
            "password": self.password
        }

    @staticmethod
    def get_all_users():
        return mongo.db.users.find({}, {'password': 0})

    @staticmethod
    def get_user_by_id(user_id):
        return mongo.db.users.find_one({"_id": user_id}, {'password': 0})

    @staticmethod
    def create_user(user_data):
        return mongo.db.users.insert_one(user_data)

    @staticmethod
    def update_user(user_id, user_data):
        return mongo.db.users.update_one({"_id": user_id}, {"$set": user_data})

    @staticmethod
    def delete_user(user_id):
        return mongo.db.users.delete_one({"_id": user_id})
    
    @staticmethod
    def get_user_by_email(email):
        return mongo.db.users.find_one({"email": email})
