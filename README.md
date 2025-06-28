# 🌿🌟 MediLeaf – Intelligent Medicinal Leaf Identifier & Natural Remedy Recommender

### 🔬 Bridging Ancient Herbal Wisdom with Modern AI Technology

MediLeaf is an advanced AI-powered web application designed to help users easily **identify medicinal plants**, **understand their healing properties**, and **get personalized natural remedies**. The system uses **machine learning**, **image classification**, and **smart assistance** to make traditional healing accessible, reliable, and tech-savvy.

---

## 📌 Project Overview

In a world where natural remedies are regaining popularity—especially during the COVID-19 pandemic—many people seek safe and verified ways to use medicinal plants. MediLeaf solves this by combining **deep learning** with **herbal knowledge**, providing:

- 🌿 Medicinal plant identification from leaf images  
- 🧪 Health condition-based remedy suggestions  
- 🗣️ Voice Assistant for hands-free use  
- 📄 PDF download of remedy instructions  
- 📱 QR Code generation for instant sharing  
- 💬 Mental health chatbot (ChatGenie)  
- 🔍 Disease-based plant search  
- 🧠 Smart recommendations from user feedback

---

## ⚙️ Tech Stack

- **Frontend:** React.js, React Router
- **Backend:** Flask (Python)
- **ML Model:** EfficientNetB2 (TensorFlow / Keras)
- **Dataset:** 12,700+ images of 80 medicinal leaf classes (Kaggle)
- **Tools Used:** Voice recognition, QR code generator, PDF exporter

---

## 🧪 How It Works (Methodology)

1. **User Uploads Image:** Upload a photo of a medicinal leaf.
2. **AI Model Prediction:** Flask backend loads the EfficientNetB2 model to classify the plant.
3. **Plant Info & Uses:** Displays scientific name, medicinal uses, and remedy preparation.
4. **Smart Features:**
   - PDF download
   - QR code for quick access
   - Voice assistant (“Tell me about Tulsi”)
   - Mental health chatbot
5. **Disease to Plant Match:** Enter disease → get suggested plants (e.g., Cold → Betel Leaf, Camphor).
6. **Personal Plant Tracker:** Track owned plants and receive remedy reminders.
7. **Feedback System:** Learns from user feedback to refine suggestions.

---

## 📂 Project Structure

├── frontend/ # React frontend
│ ├── pages/ # Home, Search, ChatGenie, Database, etc.
│ └── ...
├── backend/ # Flask backend
│ ├── app.py # Flask API server
│ ├── trained_effb2.h5 # Trained EfficientNetB2 model
│ ├── classes.txt # List of 80 plant classes
│ ├── diseases.txt # Disease-to-plant mappings
│ └── ...
├── dataset/ # Image dataset (optional)
└── README.md


---

## 🧑‍💻 Team

🎓 **Team A-2**  
🏫 *KLE Dr. M. S. Sheshgiri College of Engineering and Technology, Belagavi*  
👩‍🏫 Guided by **Prof. Madhurani Shiddibhavi**

---

## 🙌 Acknowledgements

- 📊 Dataset from Kaggle
- 🧠 TensorFlow/Keras for deep learning
- 🔥 Flask for backend API
- ⚛️ React for user interface
- 🗂️ QR, PDF, Voice libraries for user experience

---

## 🚀 Future Improvements

- 🌍 Multilingual support
- 📱 Android/iOS app
- 🌱 Integration with plant-care tips
- 🧬 Medicinal compound detection

---

## 📣 Thank You!

Feel free to ⭐ star this repo, fork it, or contribute ideas for future improvements!
