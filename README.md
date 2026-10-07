# Syntrivo 🎬

> Autonomous AI Short Video Generation Engine powered by FastAPI, Edge-TTS, and Supabase S3 Cloud Storage.

Syntrivo automates the end-to-end creation of high-impact short-form videos (Reels, TikTok, YouTube Shorts). From prompt or topic input, it orchestrates automated script writing, dynamic stock footage retrieval, high-fidelity neural voice synthesis, animated captioning, and cloud rendering with zero local disk persistence.

---

## ⚡ Features

- **Automated Script Synthesis:** Generates focused, high-retention video narratives using leading LLMs.
- **Stock Footage Matching:** Automatically retrieves relevant high-definition footage from Pexels and Pixabay.
- **Neural Audio Synthesis:** Lifelike voiceovers powered by Edge-TTS with adjustable speech rates and tones.
- **Automated Subtitles:** Synchronized, customizable animated captions built right into the composition.
- **Cloud-Native Storage:** Direct video uploads to Supabase S3 bucket (`syntrivo-videos`).
- **Zero Local Footprint:** Automated disk purging deletes temporary intermediate clips immediately post-render.

---

## 🎬 Sample Demonstration



https://github.com/user-attachments/assets/667e8a59-a249-4731-a89c-2ea1387e6e86



<div align="center">
  <video src="./assets/demo.mp4" width="360" controls></video>
</div>

Generated end-to-end via Syntrivo:
- **Topic:** Quantum Computing
- **Format:** 9:16 Vertical Video (Shorts / Reels)
- **Voiceover:** Neural Edge-TTS
- **Storage Target:** Supabase S3

---

## 🛠️ Architecture & Tech Stack

- **Backend:** Python, FastAPI, MoviePy, FFmpeg
- **Audio:** Edge-TTS
- **Cloud Storage:** Supabase (S3-compatible Object Storage via Boto3)
- **Frontend / Interface:** Modern Web UI

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone [https://github.com/pratikmakwanacode/syntrivo.git](https://github.com/pratikmakwanacode/syntrivo.git)
cd syntrivo


https://github.com/user-attachments/assets/ec419882-a3c3-4998-97ef-1a6de0d64f4c

