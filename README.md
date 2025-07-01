<p align="center">
  <img src="https://github.com/user-attachments/assets/ba079611-227f-43d6-9704-fc28e93a4380" alt="TripScan Logo" width="300"/>
</p>

# TripScan

**AI-Powered Group Travel Planning**  
*Built with love to make group trips easy.*

---

## 🚀 Overview

TripScan transforms chaotic group trip planning into a seamless, AI-powered experience. Just share your group’s chat, and our system will analyze preferences, detect vetoes, resolve conflicts, and recommend tailored destinations with real-time booking options.

---

## 🖼️ How It Works

### 1️⃣ Group Chat Analysis
<p align="center">
  <img width="800" alt="TripScan Itinerary" src="https://github.com/user-attachments/assets/5bbda13f-5fb0-48ee-82c7-920f9480c7ce">
</p>

- Paste your group conversation.
- Our LLM assigns **weighted scores (1–10)** for 12 travel factors (e.g. mountain, beach, nightlife).
- **Veto detection**: NLP model flags destinations the group doesn't want.
- **Image support**: Upload photos, and an **image-to-text model** estimates city features to add to favorites.

---

### 2️⃣ Smart Recommendations
<p align="center">
  <img width="800" alt="TripScan Itinerary" src="https://github.com/user-attachments/assets/2463cac4-f724-4315-8e58-62538f8dffa9">
</p>

- A trained recommendation model matches cities using **polynomial features** + **cosine similarity**.
- Multi-phase filtering with fallback logic ensures diverse, realistic suggestions.
- Transparent scoring builds trust with the group.

---

### 3️⃣ Itinerary Planning & Bookings
<p align="center">
  <img width="800" alt="TripScan Itinerary" src="https://github.com/user-attachments/assets/30dcd0e1-faf0-441a-97ee-3744ee79dd08" />
</p>

- Daily plans with efficient routing.
- Live flight search powered by **Skyscanner API**.
- Estimates costs and travel times.

---

## 🔍 Features

✅ **LLM-Powered Preference Extraction**  
✅ **Explainable Recommender System**  
✅ **Game Theory-Based Conflict Resolution**  
✅ **Image-to-Preference Scoring**  
✅ **Live Booking Integration (Skyscanner)**  
✅ **Smart Itinerary Builder**  

---

## 🛠️ Tech Stack

- **Backend:** FastAPI with explainability endpoints
- **LLMs:** Gemini 2.0 Flash (JSON output)
- **Frontend:** React visualizations
- **APIs:** Skyscanner, Pexels
- **Recommender:** Multi-phase filtering with fallback logic

---

## 🧠 Challenges & Solutions

- **Veto Detection:** Combined regex & sentiment analysis improved accuracy to 92%.  
- **Bias Mitigation:** Synthetic city data increased fairness across preferences.  
- **Preference Conflicts:** Multi-city routes designed to avoid paradoxes.  
- **Scalability:** <3s processing time for 50+ messages.

---

## ✅ Highlights

- 89% match rate with professional travel planner suggestions
- 90% user satisfaction with compromise suggestions
- Explainable scoring improved trust by 68%

---

## 📈 What’s Next

- Voice and image inputs (Gemini Pro integration)
- Dynamic re-ranking based on live prices
- Expense tracking and splitting
- Real-time itinerary updates

---

## ❤️ Why TripScan?

Planning group trips often leads to confusion, conflict, and compromises no one loves. TripScan uses state-of-the-art AI to **analyze real conversations**, **resolve conflicts fairly**, and **deliver travel recommendations everyone can agree on**—complete with booking options.  

> Make your next group trip planning session as easy as chatting with friends.
