"""
Agent 8: Season
Recommends planting/harvest windows using seasonal factor and weather patterns via Ollama LLM and SQLite.
"""

from datetime import datetime

class Season:
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
        seasonal_factor = input_data.get("Seasonal_Factor", "N/A")
        temperature = input_data.get("Temperature_C", "N/A")
        rainfall = input_data.get("Rainfall_mm", "N/A")
        region = input_data.get("Region", "your area")

        prompt = f"""
        For {crop} in {region}, analyze seasonal planting and harvesting suitability.
        Current conditions:
        - Temperature: {temperature}°C
        - Rainfall: {rainfall} mm
        - Seasonal Factor: {seasonal_factor}

        Recommend the best planting or harvest time and flag any timing risks.
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
