from .. import mongo


class AgriculturalProduct:
    def __init__(self, name, description, price, stock, image_url=None):
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock
        self.image_url = image_url

    # Função para criar uma instância da classe AgriculturalProduct a partir de um dicionário.
    @staticmethod
    def from_dict(data):
        return AgriculturalProduct(
            name=data.get("name"),
            description=data.get("description"),
            price=data.get("price"),
            stock=data.get("stock"),
            image_url=data.get("image_url")
        )

    # Function to convert the AgriculturalProduct object into a dictionary
    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "stock": self.stock,
            "image_url": self.image_url
        }

    @staticmethod
    def get_all_products():
        return mongo.db.products.find()

    @staticmethod
    def get_product_by_id(product_id):
        return mongo.db.products.find_one({"_id": product_id})

    @staticmethod
    def create_product(product_data):
        return mongo.db.products.insert_one(product_data)

    @staticmethod
    def update_product(product_id, product_data):
        return mongo.db.products.update_one({"_id": product_id}, {"$set": product_data})

    @staticmethod
    def delete_product(product_id):
        return mongo.db.products.delete_one({"_id": product_id})
    
    @staticmethod
    def get_products_in_stock():
        return mongo.db.products.find({"stock": {"$gt": 0}})
