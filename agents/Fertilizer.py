"""
Agent 15: Fertilizer
Recommends optimal fertilizer type and dosage using crop, soil, and yield data with Ollama LLM and SQLite.
"""

from datetime import datetime

class Fertilizer:
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
        fertilizer_used = input_data.get("Fertilizer_Usage_kg", "N/A")
        soil_ph = input_data.get("Soil_pH", "N/A")
        yield_val = input_data.get("Crop_Yield_ton", "N/A")
        region = input_data.get("Region", "your area")

        prompt = f"""
        Based on current fertilizer usage of {fertilizer_used} kg for {crop} in {region},
        - Soil pH = {soil_ph}
        - Crop yield = {yield_val} tons

        Recommend the best fertilizer types, dosage adjustments, and improvements for yield and soil health.
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
