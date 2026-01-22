import os
import json
import numpy as np
from datetime import datetime, timedelta
import random

def generate_synthetic_data():
    """Generate realistic synthetic soil and wisdom data"""
    
    # Soil types and characteristics
    soil_types = [
        "Red Loam", "Black Cotton", "Alluvial", "Laterite", 
        "Mountain", "Desert", "Peaty", "Saline", "Clay", "Sandy"
    ]
    
    crops = ["Rice", "Wheat", "Millet", "Maize", "Pulses", "Vegetables", "Fruits", "Spices"]
    
    traditional_methods = [
        "Crop Rotation", "Natural Compost", "Green Manure", "Mulching",
        "Terrace Farming", "Rainwater Harvesting", "Intercropping",
        "Agroforestry", "Zero Tillage", "Biodynamic Preparation"
    ]
    
    locations = [
        {"state": "Odisha", "lat": 20.9517, "lon": 85.0985},
        {"state": "Karnataka", "lat": 15.3173, "lon": 75.7139},
        {"state": "Rajasthan", "lat": 27.0238, "lon": 74.2179},
        {"state": "Punjab", "lat": 31.1471, "lon": 75.3412},
        {"state": "Kerala", "lat": 10.8505, "lon": 76.2711}
    ]
    
    farmer_names = [
        "Rajesh Patel", "Lakshmi Devi", "Arun Kumar", "Meera Singh",
        "Gopal Sharma", "Sunita Reddy", "Vikram Joshi", "Anjali Mehta"
    ]
    
    # Generate 50 soil samples
    soil_samples = []
    for i in range(50):
        location = random.choice(locations)
        soil_type = random.choice(soil_types)
        crop = random.choice(crops)
        method = random.sample(traditional_methods, k=random.randint(1, 3))
        
        # Generate realistic sensor data
        if soil_type == "Red Loam":
            moisture = round(random.uniform(0.25, 0.45), 2)
            ph = round(random.uniform(5.5, 6.5), 2)
            temp = round(random.uniform(25, 32), 1)
        elif soil_type == "Black Cotton":
            moisture = round(random.uniform(0.35, 0.55), 2)
            ph = round(random.uniform(7.0, 8.5), 2)
            temp = round(random.uniform(28, 35), 1)
        else:
            moisture = round(random.uniform(0.2, 0.5), 2)
            ph = round(random.uniform(5.0, 8.0), 2)
            temp = round(random.uniform(20, 35), 1)
        
        # Yield quality (reinforcement score influenced by method)
        if "Natural Compost" in method or "Crop Rotation" in method:
            yield_quality = random.choice(["good", "good", "good", "average"])
            success_count = random.randint(5, 15)
        else:
            yield_quality = random.choice(["good", "average", "average", "poor"])
            success_count = random.randint(1, 8)
        
        # Generate random date in last 5 years
        date = (datetime.now() - timedelta(days=random.randint(0, 1825))).strftime("%Y-%m-%d")
        
        soil_samples.append({
            "id": f"soil_{i+1:03d}",
            "soil_type": soil_type,
            "location": location,
            "crop_grown": crop,
            "traditional_methods": method,
            "sensor_data": {
                "moisture": moisture,
                "pH": ph,
                "temperature": temp,
                "nitrogen": round(random.uniform(0.1, 0.8), 2),
                "phosphorus": round(random.uniform(0.05, 0.6), 2),
                "potassium": round(random.uniform(0.2, 0.9), 2)
            },
            "yield_quality": yield_quality,
            "date": date,
            "success_count": success_count,
            "reinforcement_score": round(success_count / 20, 2),  # Normalized score
            "season": random.choice(["pre-monsoon", "monsoon", "post-monsoon", "winter", "summer"]),
            "farmer_feedback": random.choice([
                "Traditional method worked well",
                "Good yield this season",
                "Soil health improved",
                "Needs more composting",
                "Water retention improved"
            ])
        })
    
    # Generate 20 wisdom audio snippets
    wisdom_audio = []
    wisdom_topics = [
        ("Monsoon Preparation", [
            "Start preparing soil 2 weeks before monsoon",
            "Add organic compost to improve water retention",
            "Create proper drainage channels",
            "Use mulch to prevent soil erosion"
        ]),
        ("Soil Revival", [
            "For acidic soil, add lime or wood ash",
            "Grow green manure crops between seasons",
            "Earthworms are friends of the soil",
            "Never burn crop residue - it kills soil life"
        ]),
        ("Water Conservation", [
            "Dig small pits to capture rainwater",
            "Plant trees on farm boundaries for shade",
            "Use drip irrigation for vegetables",
            "Morning irrigation reduces evaporation"
        ]),
        ("Natural Pest Control", [
            "Neem leaves soaked in water make good pesticide",
            "Plant marigold around crops to repel insects",
            "Mix chili and garlic paste for pest spray",
            "Attract birds with perches for natural pest control"
        ])
    ]
    
    for i in range(20):
        topic, advice_list = random.choice(wisdom_topics)
        farmer = random.choice(farmer_names)
        
        wisdom_audio.append({
            "id": f"wisdom_{i+1:03d}",
            "farmer_name": farmer,
            "experience_years": random.randint(20, 60),
            "topic": topic,
            "advice": random.choice(advice_list),
            "language": "Odia/Hindi/English",
            "season_applicable": random.choice(["monsoon", "winter", "summer", "all"]),
            "soil_types_applicable": random.sample(soil_types, k=random.randint(1, 3)),
            "popularity_score": random.randint(1, 100),
            "date_recorded": (datetime.now() - timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d")
        })
    
    # Save to files
    os.makedirs("data", exist_ok=True)
    
    with open("data/soil_samples.json", "w") as f:
        json.dump(soil_samples, f, indent=2)
    
    with open("data/wisdom_audio.json", "w") as f:
        json.dump(wisdom_audio, f, indent=2)
    
    print(f"Generated {len(soil_samples)} soil samples and {len(wisdom_audio)} wisdom snippets")
    print("Data saved to data/ directory")

if __name__ == "__main__":
    generate_synthetic_data()