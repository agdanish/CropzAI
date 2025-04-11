"""
Agent 4: SupplyAnalytics
Identifies over- or under-supply regions using supply index and market data via Ollama LLM and SQLite.
"""

from datetime import datetime

class SupplyAnalytics:
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
        product = input_data.get("Product", "Unknown Product")
        supply_index = input_data.get("Supply_Index", "N/A")
        demand_index = input_data.get("Demand_Index", "N/A")
        region = input_data.get("Region", "your area")

        prompt = f"""
        Analyze the supply situation for {product} in {region}.
        - Supply Index: {supply_index}
        - Demand Index: {demand_index}

        Determine if there's oversupply or shortage and suggest marketing, logistics, or pricing adjustments.
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