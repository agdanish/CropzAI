"""
Agent 21: BudgetPlanner
Creates a cost plan for crop production and projects ROI using LLM and SQLite.
"""

from datetime import datetime

class BudgetPlanner:
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
        crop = input_data.get("Crop_Type", "Unknown Crop")
        fertilizer = input_data.get("Fertilizer_Usage_kg", "N/A")
        pesticide = input_data.get("Pesticide_Usage_kg", "N/A")
        yield_val = input_data.get("Crop_Yield_ton", "N/A")
        market_price = input_data.get("Market_Price_per_ton", "N/A")
        region = input_data.get("Region", "your area")

        prompt = f"""
        Create a simple budget plan for growing {crop} in {region}:
        - Fertilizer: {fertilizer} kg
        - Pesticide: {pesticide} kg
        - Expected Yield: {yield_val} tons
        - Market Price: ₹{market_price} per ton

        Estimate total cost, revenue, and ROI. Suggest how to reduce costs or boost profits.
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
