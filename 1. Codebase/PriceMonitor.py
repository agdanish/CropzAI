"""
Agent 2: PriceMonitor
Analyzes market and competitor pricing trends for the selected crop using Ollama LLM and SQLite.
"""

from datetime import datetime

class PriceMonitor:
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
        market_price = input_data.get("Market_Price_per_ton", "N/A")
        competitor_price = input_data.get("Competitor_Price_per_ton", "N/A")
        demand_index = input_data.get("Demand_Index", "N/A")

        prompt = f"""
        Analyze the pricing of {crop} based on:
        - Market Price per ton: ₹{market_price}
        - Competitor Price per ton: ₹{competitor_price}
        - Demand Index: {demand_index}

        Determine if the crop is competitively priced, and recommend adjustments or market strategies.
        """

        try:
            response = self.llm.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
            output_data = response["message"]["content"]
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