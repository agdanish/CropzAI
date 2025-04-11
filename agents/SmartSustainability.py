"""
Agent 22: SmartSustainability
Suggests sustainable farming practices to reduce environmental impact using Ollama LLM and SQLite.
"""

from datetime import datetime

class SmartSustainability:
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
        soil_ph = input_data.get("Soil_pH", "N/A")
        moisture = input_data.get("Soil_Moisture", "N/A")
        temperature = input_data.get("Temperature_C", "N/A")
        rainfall = input_data.get("Rainfall_mm", "N/A")
        fertilizer = input_data.get("Fertilizer_Usage_kg", "N/A")
        pesticide = input_data.get("Pesticide_Usage_kg", "N/A")
        region = input_data.get("Region", "your area")

        prompt = f"""
        Suggest sustainable practices for growing {crop} in {region}.
        Conditions:
        - Soil pH: {soil_ph}, Moisture: {moisture}%
        - Temperature: {temperature}°C, Rainfall: {rainfall} mm
        - Fertilizer: {fertilizer} kg, Pesticide: {pesticide} kg

        Recommend water-saving, soil health, carbon footprint reduction, and biodiversity-friendly methods.
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
