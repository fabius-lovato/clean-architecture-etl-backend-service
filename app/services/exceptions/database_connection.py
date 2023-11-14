
class DatabaseConnection(Exception):
    """Exception quando a conexão com a base de dados ou serviço de armazenamento falhou."""

    def __init__(self, details: str = None):
        self.message = f'Database connection failed'
        self.details = details

        super().__init__(self.message)
