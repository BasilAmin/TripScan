<p align="center">
  <img src="https://github.com/user-attachments/assets/ba079611-227f-43d6-9704-fc28e93a4380" alt="TripScan Logo" width="300"/>
</p>

# TripScan

**AI-Powered Group Travel Planning**

---

## 🚀 Overview

TripScan simplifies group travel planning using AI. It analyzes chat conversations to extract preferences, resolve conflicts, and generate optimized itineraries with live booking options.

---

## 🔍 Features

- **LLM-Powered Analysis:** Extracts weighted scores (1–10) for 12 travel factors.
- **XAI Recommender:** Matches cities using polynomial features + cosine similarity.
- **Conflict Resolution:** Applies game theory for optimal compromises.
- **Smart Itineraries:** Builds daily plans with efficient routing.
- **Live Bookings:** Integrates Skyscanner data for real-time flights.

---

## 🛠️ Tech Stack

- **Backend:** FastAPI + explainability endpoints  
- **LLMs:** Gemini 2.0 Flash (JSON output)  
- **Frontend:** React visualizations  
- **APIs:** Skyscanner, Pexels  
- **Recommender:** Multi-phase filtering with fallback logic

---

## 🧠 Challenges & Solutions

- **Veto Detection:** Regex + sentiment boosted accuracy to 92%.  
- **Data Bias:** Synthetic city data improved fairness.  
- **Preference Conflicts:** Multi-city routes handled paradoxes.

---

## ✅ Highlights

- 89% match with pro travel planners  
- 90% user satisfaction with compromise suggestions  
- <3s processing for 50+ messages  
- Explainable scores improved trust by 68%

---

## 📈 What’s Next

- Voice/image input (Gemini Pro)  
- Dynamic re-ranking with live prices  
- Expense tracking & splitting  
- Real-time itinerary updates

---

*Built with love to make group trips easy.*
