"""
Agent 25: LanguageAgent
Translates and simplifies agent outputs into the farmer’s preferred language using LLM and SQLite.
"""

from datetime import datetime

class LanguageAgent:
    def __init__(self, db_conn=None, llm=None):
        self.db_conn = db_conn
        self.llm = llm
        self.create_tables()

    def create_tables(self):
        if self.db_conn:
            self.db_conn.execute("""
                CREATE TABLE IF NOT EXISTS agent_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    agent_name TEXT,
                    input_data TEXT,
                    output_data TEXT,
                    timestamp TEXT
                )
            """)
            self.db_conn.execute("""
                CREATE TABLE IF NOT EXISTS translation_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    original_text TEXT,
                    translated_text TEXT,
                    target_language TEXT,
                    timestamp TEXT
                )
            """)
            self.db_conn.commit()

    def analyze(self, input_data, session_id=None):
        original_text = input_data.get("output_text", "")
        target_language = input_data.get("language", "English")

        prompt = f"""
        Translate the following farming advice into {target_language}.
        Make it simple, easy to understand, and relevant for rural farmers:

        {original_text}
        """

        try:
            translated_text = self.llm.chat(prompt=prompt)
        except Exception as e:
            translated_text = f"Error translating: {e}"

        self.log_to_db(input_data, translated_text, session_id)
        return translated_text

    def log_to_db(self, input_data, translated_text, session_id):
        if self.db_conn:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.db_conn.execute(
                "INSERT INTO agent_logs (session_id, agent_name, input_data, output_data, timestamp) VALUES (?, ?, ?, ?, ?)",
                (session_id, self.__class__.__name__, str(input_data), translated_text, timestamp)
            )
            self.db_conn.execute(
                "INSERT INTO translation_logs (session_id, original_text, translated_text, target_language, timestamp) VALUES (?, ?, ?, ?, ?)",
                (session_id, input_data.get("output_text", ""), translated_text, input_data.get("language", "English"), timestamp)
            )
            self.db_conn.commit()
