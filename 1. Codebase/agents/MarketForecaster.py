"""
Agent 24: MarketForecaster
Forecasts future crop prices using market trends, supply/demand, and economic indicators via LLM and SQLite.
"""

from datetime import datetime

class MarketForecaster:
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
        supply_index = input_data.get("Supply_Index", "N/A")
        economic_indicator = input_data.get("Economic_Indicator", "N/A")
        market_price = input_data.get("Market_Price_per_ton", "N/A")
        competitor_price = input_data.get("Competitor_Price_per_ton", "N/A")

        prompt = f"""
        Forecast the price trend for {product}.
        Indicators:
        - Demand Index: {demand_index}
        - Supply Index: {supply_index}
        - Economic Indicator: {economic_indicator}
        - Current Market Price: ₹{market_price}
        - Competitor Price: ₹{competitor_price}

        Provide a detailed market outlook and pricing recommendation.
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
