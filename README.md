# 🌱 Bhu-Smruti: Soil Wisdom Memory Bank

**Hackathon:** Pan-IIT Convolve 4.0 - Qdrant Track  
**Team:** [Bhumi]  
**Track:** Search, Memory, and Recommendations for Societal Impact  


---

## 🎥 **Watch the Demo **
[![Demo ] http://localhost:8501/ 




## 📖 **Table of Contents**
- [Problem Statement](#-problem-statement)
- [Our Solution](#-our-solution)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Usage](#-usage)
- [Qdrant Implementation](#-qdrant-implementation)
- [Hackathon Criteria](#-hackathon-criteria)
- [Team](#-team)
- [License](#-license)

---

## 🌍 **Problem Statement**

**Indigenous soil knowledge is disappearing** at an alarming rate. Each time an elder farmer passes away, **centuries of traditional wisdom** about soil, crops, and climate adaptation is lost forever.

### **Key Challenges:**
1. **Vanishing Knowledge:** Elder farmers' expertise isn't documented systematically
2.  **Climate Change:** Traditional methods need adaptation to new conditions  
3.  **Fragmented Data:** Soil images, sensor readings, and traditional wisdom exist in isolation
4.  **No Collective Memory:** Successful farming practices aren't remembered and reinforced

---

##  **Our Solution**

**Bhu-Smruti** (भू-स्मृति - "Earth Memory") is an **AI-powered memory system** that preserves indigenous soil knowledge and provides intelligent recommendations to farmers.

### **How It Works:**
1. **Store** multimodal soil data (text descriptions, sensor readings, traditional wisdom)
2. **Search** for similar soil conditions using Qdrant's vector similarity
3. **Recommend** proven traditional methods based on successful cases
4. **Reinforce** memory when methods work, creating a self-improving system

---

## ✨ **Features**

| Feature | Description | Tech Used |
|---------|-------------|-----------|
| **🔍 Multimodal Search** | Find similar soils using natural language queries | Qdrant + Sentence Transformers |
| **👴 Wisdom Preservation** | Store and retrieve elder farmers' audio/text advice | Vector embeddings |
| **💡 Smart Recommendations** | AI suggests methods based on similar successful cases | Similarity search + filtering |
| **🔄 Memory Reinforcement** | System learns what works and improves over time | Success tracking in Qdrant |
| **📊 Analytics Dashboard** | Visualize soil health trends and method effectiveness | Plotly + Streamlit |

---

## 🛠️ **Tech Stack**

**Backend & AI:**
- **Qdrant** - Vector database for similarity search and memory
- **Sentence Transformers** - Text embedding generation
- **Python** - Backend logic and data processing

**Frontend:**
- **Streamlit** - Interactive web application
- **Plotly** - Data visualizations
- **Pandas** - Data manipulation

**Data:**
- Synthetic soil datasets (50+ samples)
- Traditional wisdom snippets (20+ entries)
- Soil sensor data simulation

---
  **Installation**

```bash
# 1. Clone the repository
git clone https://github.com/your-username/bhu-smruti.git
cd bhu-smruti

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate sample data
python setup.py

# 4. Run the application
streamlit run app.py
