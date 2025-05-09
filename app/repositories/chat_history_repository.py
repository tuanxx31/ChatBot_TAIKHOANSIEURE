class ChatHistoryRepository:
    def __init__(self, conn):
        self.conn = conn

    def save(self, user_input, bot_response):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO chat_history (user_input, bot_response) VALUES (%s, %s)",
            (user_input, bot_response)
        )
        self.conn.commit()
