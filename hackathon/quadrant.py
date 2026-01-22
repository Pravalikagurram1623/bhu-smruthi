from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams
from qdrant_client.http.models import PointStruct, Filter, FieldCondition, MatchValue
import json
import os
from models.embeddings import EmbeddingGenerator

class BhuSmrutiQdrant:
    def __init__(self, use_cloud=True):
        self.embedding_gen = EmbeddingGenerator()
        
        if use_cloud:
            # For Qdrant Cloud (sign up at cloud.qdrant.io)
            # You'll need to set these as environment variables
            self.client = QdrantClient(
                url=os.getenv("QDRANT_URL", "https://your-instance.cloud.qdrant.io"),
                api_key=os.getenv("QDRANT_API_KEY", "your-api-key")
            )
        else:
            # For local Docker container
            self.client = QdrantClient(host="localhost", port=6333)
        
        self.soil_collection = "soil_samples"
        self.wisdom_collection = "wisdom_audio"
        
    def setup_collections(self):
        """Create collections in Qdrant if they don't exist"""
        
        # Soil samples collection
        try:
            self.client.get_collection(self.soil_collection)
            print(f"Collection '{self.soil_collection}' already exists")
        except:
            self.client.create_collection(
                collection_name=self.soil_collection,
                vectors_config=VectorParams(
                    size=388,  # 384 (MiniLM) + 4 (sensor features)
                    distance=Distance.COSINE
                )
            )
            print(f"Created collection '{self.soil_collection}'")
        
        # Wisdom audio collection
        try:
            self.client.get_collection(self.wisdom_collection)
            print(f"Collection '{self.wisdom_collection}' already exists")
        except:
            self.client.create_collection(
                collection_name=self.wisdom_collection,
                vectors_config=VectorParams(
                    size=384,  # MiniLM embedding size
                    distance=Distance.COSINE
                )
            )
            print(f"Created collection '{self.wisdom_collection}'")
    
    def load_initial_data(self):
        """Load synthetic data into Qdrant"""
        with open("data/soil_samples.json", "r") as f:
            soil_samples = json.load(f)
        
        with open("data/wisdom_audio.json", "r") as f:
            wisdom_data = json.load(f)
        
        # Upload soil samples
        soil_points = []
        for sample in soil_samples:
            embedding = self.embedding_gen.generate_soil_embedding(sample)
            
            point = PointStruct(
                id=int(sample["id"].split("_")[1]),  # soil_001 -> 1
                vector=embedding,
                payload={
                    "id": sample["id"],
                    "soil_type": sample["soil_type"],
                    "location": sample["location"],
                    "crop_grown": sample["crop_grown"],
                    "traditional_methods": sample["traditional_methods"],
                    "sensor_data": sample["sensor_data"],
                    "yield_quality": sample["yield_quality"],
                    "date": sample["date"],
                    "success_count": sample["success_count"],
                    "reinforcement_score": sample["reinforcement_score"],
                    "season": sample["season"],
                    "farmer_feedback": sample["farmer_feedback"]
                }
            )
            soil_points.append(point)
        
        self.client.upsert(
            collection_name=self.soil_collection,
            points=soil_points
        )
        print(f"Loaded {len(soil_points)} soil samples")
        
        # Upload wisdom audio
        wisdom_points = []
        for wisdom in wisdom_data:
            embedding = self.embedding_gen.generate_wisdom_embedding(wisdom)
            
            point = PointStruct(
                id=int(wisdom["id"].split("_")[1]),  # wisdom_001 -> 1
                vector=embedding,
                payload={
                    "id": wisdom["id"],
                    "farmer_name": wisdom["farmer_name"],
                    "experience_years": wisdom["experience_years"],
                    "topic": wisdom["topic"],
                    "advice": wisdom["advice"],
                    "language": wisdom["language"],
                    "season_applicable": wisdom["season_applicable"],
                    "soil_types_applicable": wisdom["soil_types_applicable"],
                    "popularity_score": wisdom["popularity_score"],
                    "date_recorded": wisdom["date_recorded"]
                }
            )
            wisdom_points.append(point)
        
        self.client.upsert(
            collection_name=self.wisdom_collection,
            points=wisdom_points
        )
        print(f"Loaded {len(wisdom_points)} wisdom snippets")
    
    def search_similar_soil(self, query_text, sensor_data=None, season_filter=None, limit=5):
        """Search for similar soil samples"""
        query_vector = self.embedding_gen.generate_query_embedding(query_text, sensor_data)
        
        # Build filter if needed
        query_filter = None
        if season_filter:
            query_filter = Filter(
                must=[FieldCondition(key="season", match=MatchValue(value=season_filter))]
            )
        
        results = self.client.search(
            collection_name=self.soil_collection,
            query_vector=query_vector,
            query_filter=query_filter,
            limit=limit,
            with_payload=True,
            with_vectors=False
        )
        
        return results
    
    def search_wisdom(self, query_text, soil_type_filter=None, limit=5):
        """Search for relevant wisdom snippets"""
        query_vector = self.embedding_gen.generate_query_embedding(query_text)
        
        query_filter = None
        if soil_type_filter:
            query_filter = Filter(
                must=[FieldCondition(
                    key="soil_types_applicable", 
                    match=MatchValue(value=soil_type_filter)
                )]
            )
        
        results = self.client.search(
            collection_name=self.wisdom_collection,
            query_vector=query_vector,
            query_filter=query_filter,
            limit=limit,
            with_payload=True,
            with_vectors=False
        )
        
        return results
    
    def get_recommendations(self, soil_sample_id, limit=3):
        """Get recommendations based on similar successful cases"""
        # First, get the soil sample
        soil_sample = self.client.retrieve(
            collection_name=self.soil_collection,
            ids=[int(soil_sample_id.split("_")[1])],
            with_payload=True,
            with_vectors=True
        )[0]
        
        # Search for similar soils with good yield
        query_filter = Filter(
            must=[
                FieldCondition(key="yield_quality", match=MatchValue(value="good")),
                FieldCondition(key="soil_type", match=MatchValue(value=soil_sample.payload["soil_type"]))
            ]
        )
        
        results = self.client.search(
            collection_name=self.soil_collection,
            query_vector=soil_sample.vector,
            query_filter=query_filter,
            limit=limit,
            with_payload=True,
            with_vectors=False
        )
        
        # Extract successful methods
        recommendations = []
        for result in results:
            if result.payload["id"] != soil_sample_id:  # Exclude self
                for method in result.payload["traditional_methods"]:
                    if method not in recommendations:
                        recommendations.append(method)
                        if len(recommendations) >= 5:
                            break
        
        return recommendations[:5]
    
    def reinforce_memory(self, soil_sample_id, worked_well=True):
        """Reinforce memory when a method works well"""
        # Get current success count
        soil_sample = self.client.retrieve(
            collection_name=self.soil_collection,
            ids=[int(soil_sample_id.split("_")[1])],
            with_payload=True
        )[0]
        
        current_count = soil_sample.payload.get("success_count", 0)
        new_count = current_count + 1 if worked_well else current_count
        
        # Update the point
        self.client.set_payload(
            collection_name=self.soil_collection,
            payload={
                "success_count": new_count,
                "reinforcement_score": round(new_count / 20, 2),
                "farmer_feedback": "Method confirmed effective" if worked_well else "Needs adjustment"
            },
            points=[int(soil_sample_id.split("_")[1])]
        )
        
        print(f"Reinforced memory for {soil_sample_id}: success_count = {new_count}")
        return new_count
    
    def get_soil_stats(self):
        """Get statistics about soil data"""
        # Get all points (simplified - in production would use scroll)
        points = self.client.scroll(
            collection_name=self.soil_collection,
            limit=100,
            with_payload=True
        )[0]
        
        stats = {
            "total_samples": len(points),
            "soil_types": {},
            "avg_reinforcement": 0,
            "successful_methods": []
        }
        
        method_counts = {}
        total_reinforcement = 0
        
        for point in points:
            soil_type = point.payload["soil_type"]
            stats["soil_types"][soil_type] = stats["soil_types"].get(soil_type, 0) + 1
            
            total_reinforcement += point.payload.get("reinforcement_score", 0)
            
            for method in point.payload["traditional_methods"]:
                method_counts[method] = method_counts.get(method, 0) + 1
        
        if points:
            stats["avg_reinforcement"] = round(total_reinforcement / len(points), 2)
        
        # Top 5 successful methods
        stats["successful_methods"] = sorted(
            method_counts.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:5]
        
        return stats