Чудово. Нижче — **повноцінний, коректний, інженерний README.md**, оформлений **на рівні Universe Group / Cleaner Guru**, без води, з акцентом на продуктове мислення, алгоритми, UX і масштабованість.
Можеш **копіювати 1:1** у `README.md`.

---

# 🧹 Cleaner Guru — Smart Gallery Cleanup Engine

> **Intelligent photo gallery analysis & cleanup system**
> Built as a real-world engineering task for **Cleaner Guru / Universe Group**

---

## 📌 Overview

**Cleaner Guru** is an intelligent photo gallery cleanup system that scans a user’s photo library, detects redundant and low-quality media, and produces **clear, actionable recommendations** on what can be safely removed or archived.

The project is designed not as a simple script, but as a **product-ready backend + UI prototype**, focusing on:

* real-world photo gallery problems
* performance on large datasets
* explainable and user-friendly cleanup suggestions

---

## 🎯 Problem Statement

Modern photo galleries quickly become cluttered with:

* exact duplicates
* nearly identical shots
* burst photo sequences
* blurry or dark images
* screenshots and messenger media
* oversized photos wasting storage

Manual cleanup is slow, error-prone, and frustrating.

**Cleaner Guru automates this process**, grouping photos by semantic and technical similarity and suggesting the *best possible cleanup actions* — without deleting anything automatically.

---

## 🧠 Core Idea & Philosophy

* **Nothing is deleted automatically**
* The system only **suggests**, the user decides
* Each recommendation is **explainable**
* “KEEP” is always shown clearly
* Designed to scale from **dozens to thousands of photos**

This mirrors how real production cleanup tools work.

---

## 🧩 System Architecture

```
photos/                      → user gallery input
│
├── scanner.py               → metadata extraction
│
├── analysis modules:
│   ├── duplicates.py        → exact hash duplicates
│   ├── similar.py           → perceptual similarity (pHash)
│   ├── burst.py             → time-based burst detection
│   ├── quality.py           → blur detection (OpenCV)
│   ├── dark.py              → low brightness detection
│   ├── large.py             → oversized images
│   ├── screenshots.py       → screenshots & messenger media
│
├── ranking.py               → best photo selection logic
│
├── result.json              → structured cleanup result
│
└── ui (Flask):
    ├── app.py               → web server
    ├── templates/index.html → UI
    └── static/              → CSS + JS
```

---

## 🔍 Implemented Detection & Grouping Algorithms

### 1️⃣ Exact Duplicates

* SHA-256 file hashing
* 100% identical images grouped together
* Largest / best-quality image marked as **KEEP**

### 2️⃣ Similar Photos

* Perceptual hashing (pHash)
* Hamming distance threshold
* Detects visually similar but not identical images

### 3️⃣ Burst Photos

* Timestamp-based clustering
* Groups rapid sequences (e.g. multiple shots in seconds)
* Keeps the best-quality frame

### 4️⃣ Blurry Photos

* OpenCV Laplacian variance
* Low sharpness = blur candidate
* Blur score is shown in UI

### 5️⃣ Dark Photos

* Average brightness analysis
* Flags underexposed images

### 6️⃣ Large Photos

* Detects storage-heavy images
* Prioritizes cleanup by memory impact

### 7️⃣ Screenshots / Messenger Media

* Filename patterns
* Resolution heuristics
* Suggested action: **archive**, not delete

---

## ⭐ Smart Ranking System

When multiple photos belong to one group, the system ranks them using:

* resolution
* file size
* sharpness
* visual quality heuristics

The **best photo is always shown first as KEEP**.

---

## 🖥 Web UI (Flask)

A lightweight web interface for human-friendly review:

* Visual grouping
* Clear KEEP / SUGGEST DELETE separation
* Lazy-loaded previews
* Estimated freed storage
* Group counters

**No frontend frameworks** — simple, readable, and fast.

---

## 🚀 How to Run

### 1️⃣ Create virtual environment

```bash
python -m venv .venv
source .venv/Scripts/activate   # Windows (Git Bash)
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Place photos

Put test images into:

```
photos/
```

### 4️⃣ Run analysis

```bash
python src/main.py
```

This generates:

```
result.json
```

### 5️⃣ Launch UI

```bash
python src/ui/app.py
```

Open in browser:

```
http://127.0.0.1:5000
```

---

## ⚡ Performance Considerations

* Streaming photo scanning (generator-based)
* No full image loading unless required
* Hashing avoids pixel-level comparisons
* Designed to handle **thousands of photos**

---

## 🧪 Why This Is Production-Ready Thinking

✔ Clear separation of concerns
✔ Extensible architecture
✔ No hardcoded UI assumptions
✔ Human-in-the-loop decision making
✔ Safe-by-design cleanup suggestions

This mirrors how **real mobile cleanup products** are built internally.

---

## 🔮 Possible Improvements

* ML embeddings for semantic clustering
* Face detection / people grouping
* Video support
* Mobile-native UI
* User feedback loop for ranking