
# classes começam com letra maiúscula
class AlunoModelo:
    def __init__(self, nome: str, CPF: int, idade: int, email: str, endereco: str):
        self.nome = nome
        self.CPF = CPF
        self.idade = idade
        self.email = email
        self.endereco = endereco
        
        