# 🛰️ Zero-Shot Image Anomaly Detection 

A lightweight implementation of zero-shot anomaly detection using latent-space feature extraction and K-Nearest Neighbors (KNN)–based anomaly scoring.
The project focuses on detecting defects in images without training on anomalous samples, making it suitable for industrial and real-world inspection tasks where anomalies are rare.

--- 

🚀 Project Overview

Zero-Shot Anomaly Detection (ZSAD) aims to detect abnormal regions without any anomalous examples during training.
This project uses:

Latent space embeddings (from pretrained neural networks)

Normal-only training images

K-NN distance‐based anomaly scoring

Visualization notebooks for domains such as:

Hazelnut

Toothbrush

You can train models for new categories by providing "good" (normal) sample images.

📂 Repository Structure
.
├── app.py                         # Streamlit-based demo app
├── about.py                       # About section for UI
├── knn_hazelnut_good_model.pkl    # Saved normal model for Hazelnut
├── knn_toothbrush_good_model.pkl  # Saved normal model for Toothbrush
├── LatentSpace_Hazelnut.ipynb     # Notebook for Hazelnut anomaly demo
├── LatentSpace_toothbrush.ipynb   # Notebook for Toothbrush anomaly demo
├── requirements.txt               # Dependencies
└── README.md                      # Project documentation

🔍 How It Works
1. Feature Extraction

Images are passed through a pretrained CNN to obtain latent space vectors.

2. Normal Data Modeling

Only normal (good) images are used.

A KNN model is fit on the latent embeddings to learn what “normal” looks like.

3. Anomaly Scoring

For a test image:

Extract its latent vector

Compute distance to nearest neighbors in normal space

Large distance → anomaly detected

4. Visualization

Notebooks generate:

Embedding plots

Reconstruction/feature maps

Anomaly heatzones

🖥️ Running the Streamlit App
Install dependencies:
pip install -r requirements.txt

Run the app:
streamlit run app.py


You can choose the category (hazelnut/toothbrush) and upload an image to test if it contains anomalies.

📘 Notebooks Included
🔹 Hazelnut Latent Space Notebook

LatentSpace_Hazelnut.ipynb

Loads hazelnut good images

Computes latent embeddings

Fits KNN model

Tests anomalies

Visualizes anomaly scores

🔹 Toothbrush Latent Space Notebook

LatentSpace_toothbrush.ipynb

Same pipeline as above

Demonstrates the generalization of the method

📦 Models Included
Model File	Description
knn_hazelnut_good_model.pkl	KNN model trained only on hazelnut normal images
knn_toothbrush_good_model.pkl	KNN model trained on toothbrush normal samples

These models can be used directly via the Streamlit app.

🛠️ Tech Stack

Python

PyTorch / Torchvision

Scikit-learn

NumPy / Pandas

Streamlit

Matplotlib / Plotly

📌 Zero-Shot Advantage

✔ No need for defect images
✔ Works with small datasets
✔ Extensible to any new category
✔ Suitable for real-time inspection systems
