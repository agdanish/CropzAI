"""
Agent 3: DemandTrend
Forecasts future crop demand using demand index, consumer trends, and seasonality via Ollama LLM and SQLite.
"""

from datetime import datetime

class DemandTrend:
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
        demand_index = input_data.get("Demand_Index", "N/A")
        consumer_trend = input_data.get("Consumer_Trend_Index", "N/A")
        seasonal_factor = input_data.get("Seasonal_Factor", "N/A")

        prompt = f"""
        Forecast the demand for {product} based on:
        - Demand Index: {demand_index}
        - Consumer Trend Index: {consumer_trend}
        - Seasonal Factor: {seasonal_factor}

        Indicate if demand is rising, falling, or stable and suggest any marketing or planning actions.
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