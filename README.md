# 🧹 Cleaner Guru — Intelligent Gallery Cleanup System

> **Cleaner Guru** is an intelligent system for analyzing, grouping, and optimizing a user’s photo gallery.
> The goal is to automatically detect redundant, low-quality, and non-essential images and provide **clear, explainable recommendations** for cleanup — without deleting anything automatically.

---

## 📌 Problem Statement

Modern users store **thousands of photos** on their devices. Over time, galleries become cluttered with:

* Exact duplicates
* Near-identical photos (bursts, retries)
* Blurry or dark images
* Screenshots and messenger images
* Large files wasting storage

Manual cleanup is time-consuming and error-prone.
**Cleaner Guru** solves this problem by combining **efficient algorithms, heuristics, and UX-focused decisions** into a single system.

---

## 🎯 Project Goals

* Scan a gallery containing **hundreds or thousands of images**
* Automatically **group similar and redundant photos**
* Detect **low-quality images**
* Provide **clear recommendations** for cleanup
* Ensure **high performance and explainability**
* Present results in a **user-friendly interface**

---

## 🧠 System Overview

The system follows a **pipeline architecture**:

```
Scan → Enrich → Analyze → Group → Rank → Recommend → Visualize
```

Each step is isolated, testable, and replaceable.

---

## 🏗 Architecture

```
cleaner_guru/
├── photos/                # Input gallery
├── src/
│   ├── cleaner/
│   │   ├── scanner.py     # Photo scanning & metadata extraction
│   │   ├── duplicates.py # Exact duplicate detection
│   │   ├── similar.py    # Perceptual hash similarity
│   │   ├── burst.py      # Burst / series detection
│   │   ├── quality.py    # Blur detection
│   │   ├── dark.py       # Dark image detection
│   │   ├── large.py      # Large file detection
│   │   ├── screenshots.py# Screenshots & messenger images
│   │   ├── ranking.py    # Photo quality ranking
│   │   └── models.py     # Unified Photo data model
│   ├── app.py             # Flask UI
│   └── main.py            # CLI entry point
├── result.json            # Structured analysis output
├── requirements.txt
└── README.md
```

---

## 📷 Photo Data Model

Each photo is represented by a single unified model:

```python
Photo(
    path: str,
    size_bytes: int,
    width: int,
    height: int,
    sha256: str,
    phash: str,
    timestamp: datetime,
    blur: float
)
```

This allows all algorithms to operate on the **same enriched object**, improving consistency and performance.

---

## 🔍 Implemented Algorithms

### 1️⃣ Exact Duplicates

* **Algorithm:** SHA-256 hashing
* **Why:** Guarantees 100% accuracy
* **Result:** Groups of identical files

---

### 2️⃣ Similar Photos

* **Algorithm:** Perceptual Hash (pHash)
* **Metric:** Hamming distance
* **Use case:** Same scene, small changes (angle, exposure)

---

### 3️⃣ Burst / Series Detection

* **Algorithm:** Timestamp clustering
* **Logic:** Photos taken within short time windows
* **UX goal:** Keep best photo, remove the rest

---

### 4️⃣ Blurry Photos

* **Algorithm:** Variance of Laplacian (OpenCV)
* **Output:** Numeric blur score
* **Explainable:** Higher blur → lower quality

---

### 5️⃣ Dark Photos

* **Algorithm:** Mean brightness threshold
* **Use case:** Accidental night shots, unusable images

---

### 6️⃣ Large Files

* **Metric:** File size (MB)
* **Goal:** Highlight high storage impact images

---

### 7️⃣ Screenshots & Messenger Images

* **Detection:** Filename patterns + aspect ratio heuristics
* **Suggested action:** Archive instead of delete

---

## 🧮 Photo Ranking (Smart Decision Logic)

Instead of choosing photos only by size, **Cleaner Guru ranks photos by quality**:

Factors:

* Resolution
* File size
* Blur score
* Sharpness

This ensures the system **keeps the best possible image** in every group.

---

## 📊 Output Format (result.json)

The system produces a structured, machine-readable output:

```json
{
  "type": "similar_photos",
  "keep": "...",
  "suggest_delete": [...],
  "count": 9
}
```

This format allows:

* UI rendering
* Future API integration
* Easy extension (confidence score, labels, ML)

---

## 🖥 User Interface (Flask)

A lightweight Flask UI is provided:

* Visual grouping (KEEP vs DELETE)
* Image previews
* Estimated freed storage
* Zero automatic deletion (safe by design)

> UX principle: **The user is always in control**

---

## ⚡ Performance Considerations

* Generator-based scanning (low memory usage)
* Hashing used before pixel-level operations
* One-pass enrichment
* Designed to scale to **thousands of photos**

---

## 🧪 How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Put photos into `/photos`

```text
photos/
 ├── img1.jpg
 ├── img2.jpg
```

### 3. Run analysis

```bash
python src/main.py
```

### 4. Launch UI

```bash
python src/ui/app.py
```

Open browser at:

```
http://127.0.0.1:5000
```

---

## 🚀 Possible Future Improvements

* Confidence score per recommendation
* ML-based image embeddings (CLIP)
* Face detection & grouping
* Mobile integration
* Real delete / archive actions
* Cloud-scale processing

---

## 🧠 Engineering Mindset

This project was designed not as a script, but as a **scalable product prototype**, focusing on:

* Explainability
* User trust
* Performance
* Clean architecture
* Extensibility

---

## ✅ Conclusion

**Cleaner Guru** demonstrates how algorithmic thinking, software engineering practices, and UX considerations can be combined to solve a real-world problem.

This is not just a cleanup tool — it is a **decision support system** for managing personal media efficiently.

---
