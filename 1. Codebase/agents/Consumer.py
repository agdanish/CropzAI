"""
Agent 9: Consumer
Analyzes consumer trends and preferences for the selected crop using LLM and SQLite.
"""

from datetime import datetime

class Consumer:
    def __init__(self, db_conn=None, llm=None):
        self.db_conn = db_conn
        self.llm = llm
        self.create_table()

    def create_table(self):
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
            self.db_conn.commit()

    def analyze(self, input_data, session_id=None):
        crop = input_data.get("Product", "Unknown Product")
        consumer_index = input_data.get("Consumer_Trend_Index", "N/A")
        demand_index = input_data.get("Demand_Index", "N/A")
        region = input_data.get("Region", "your area")

        prompt = f"""
        Evaluate the consumer interest and trend for {crop} in {region}.
        - Consumer Trend Index: {consumer_index}
        - Demand Index: {demand_index}

        Is the crop in demand among consumers? Suggest actions like branding, marketing, or switching crops if needed.
        """

        try:
            output_data = self.llm.chat(prompt=prompt)
        except Exception as e:
            output_data = f"Error generating LLM response: {e}"

        self.log_to_db(input_data, output_data, session_id)
        return output_data

    def log_to_db(self, input_data, output_data, session_id):
        if self.db_conn:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.db_conn.execute(
                "INSERT INTO agent_logs (session_id, agent_name, input_data, output_data, timestamp) VALUES (?, ?, ?, ?, ?)",
                (session_id, self.__class__.__name__, str(input_data), str(output_data), timestamp)
            )
            self.db_conn.commit()
