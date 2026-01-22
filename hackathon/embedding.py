import numpy as np
from sentence_transformers import SentenceTransformer
import json

class EmbeddingGenerator:
    def __init__(self):
        # Use lightweight model for demo
        self.text_model = SentenceTransformer('all-MiniLM-L6-v2')
        
    def generate_soil_embedding(self, soil_data):
        """Generate embedding vector for soil sample"""
        # Create text description for embedding
        text_description = f"""
        Soil type: {soil_data['soil_type']}
        Location: {soil_data['location']['state']}
        Crop: {soil_data['crop_grown']}
        Methods: {', '.join(soil_data['traditional_methods'])}
        Moisture: {soil_data['sensor_data']['moisture']}
        pH: {soil_data['sensor_data']['pH']}
        Temperature: {soil_data['sensor_data']['temperature']}
        Season: {soil_data['season']}
        Yield: {soil_data['yield_quality']}
        """
        
        # Generate embedding
        embedding = self.text_model.encode(text_description)
        
        # Add sensor data to embedding (simple concatenation)
        sensor_features = np.array([
            soil_data['sensor_data']['moisture'],
            soil_data['sensor_data']['pH'],
            soil_data['sensor_data']['temperature'],
            soil_data['success_count'] / 20,  # Normalized
        ])
        
        # Combine text embedding with sensor features
        combined = np.concatenate([embedding, sensor_features])
        
        return combined.tolist()
    
    def generate_wisdom_embedding(self, wisdom_data):
        """Generate embedding for wisdom audio snippet"""
        text_for_embedding = f"""
        Topic: {wisdom_data['topic']}
        Advice: {wisdom_data['advice']}
        Farmer: {wisdom_data['farmer_name']} with {wisdom_data['experience_years']} years experience
        Season: {wisdom_data['season_applicable']}
        Soil types: {', '.join(wisdom_data['soil_types_applicable'])}
        """
        
        embedding = self.text_model.encode(text_for_embedding)
        return embedding.tolist()
    
    def generate_query_embedding(self, query_text, sensor_data=None):
        """Generate embedding for user query"""
        if sensor_data:
            query_with_sensors = f"{query_text} Moisture: {sensor_data.get('moisture', 0)} pH: {sensor_data.get('pH', 7)}"
            embedding = self.text_model.encode(query_with_sensors)
            
            if sensor_data:
                sensor_features = np.array([
                    sensor_data.get('moisture', 0.3),
                    sensor_data.get('pH', 7.0),
                    sensor_data.get('temperature', 30),
                    0  # Placeholder for success count
                ])
                combined = np.concatenate([embedding, sensor_features])
                return combined.tolist()
        
        embedding = self.text_model.encode(query_text)
        return embedding.tolist()