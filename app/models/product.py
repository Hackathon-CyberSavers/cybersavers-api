from .. import mongo

class ProdutoAgricola:
    def __init__(self, nome, descricao, preco, estoque, image_url=None):
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.estoque = estoque
        self.image_url = image_url

    # Função para criar uma instância da classe ProdutoAgricola a partir de um dicionário
    @staticmethod
    def from_dict(data):
        return ProdutoAgricola(
            nome=data.get("nome"),
            descricao=data.get("descricao"),
            preco=data.get("preco"),
            estoque=data.get("estoque"),
            image_url=data.get("image_url")
        )

    # Função para transformar o objeto ProdutoAgricola em um dicionário
    def to_dict(self):
        return {
            "nome": self.nome,
            "descricao": self.descricao,
            "preco": self.preco,
            "estoque": self.estoque,
            "image_url": self.image_url
        }

    @staticmethod
    def obter_todos_produtos():
        return mongo.db.produtos.find()

    @staticmethod
    def obter_produto_por_id(produto_id):
        return mongo.db.produtos.find_one({"_id": produto_id})

    @staticmethod
    def criar_produto(dados_produto):
        return mongo.db.produtos.insert_one(dados_produto)

    @staticmethod
    def atualizar_produto(produto_id, dados_produto):
        return mongo.db.produtos.update_one({"_id": produto_id}, {"$set": dados_produto})

    @staticmethod
    def deletar_produto(produto_id):
        return mongo.db.produtos.delete_one({"_id": produto_id})
    
    @staticmethod
    def obter_produtos_em_estoque():
        return mongo.db.produtos.find({"estoque": {"$gt": 0}})
