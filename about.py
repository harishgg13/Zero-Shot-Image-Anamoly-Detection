import streamlit as st

st.markdown("""
<h1>About This Project</h1>

<p>
<strong>Zero-Shot Image Anomaly Detection</strong> is a system designed to detect and identify defects in images without the need for large labeled datasets. 
By leveraging self-supervised learning and visual embedding models, the system can differentiate between normal and defective samples—even when encountering unseen defect variations.
</p>

<p>This project is ideal for <strong>manufacturing quality inspection, automation systems, machine learning researchers, and quality engineers</strong> looking to implement efficient visual inspection workflows.</p>

<hr>

<h2>Key Features</h2>
<ul>
  <li><strong>Zero-Shot Learning:</strong> Requires only normal samples for training—no manual defect labeling needed.</li>
  <li><strong>Embedding-Based Detection:</strong> Uses DINO-ViT (Vision Transformer) to create powerful image feature embeddings.</li>
  <li><strong>Defect Classification:</strong> Identifies unseen defects based on similarity scores.</li>
  <li><strong>Multi-Class Product Support:</strong> Tested with toothbrush defects and hazelnut defects (hole, crack, cut, etc.).</li>
  <li><strong>Visual Insight Tools:</strong> Heatmaps and distance scoring help interpret model decisions.</li>
</ul>

<hr>

<h2>Technology Stack</h2>
<ul>
  <li><strong>Backend & Machine Learning:</strong> Python, PyTorch, FAISS</li>
  <li><strong>Model:</strong> DINO ViT-B/8 pretrained transformer</li>
  <li><strong>Data Processing:</strong> NumPy, OpenCV, Pillow</li>
  <li><strong>Visualization:</strong> Matplotlib, Seaborn, Plotly</li>
</ul>

<hr>

<h2>How It Works</h2>
<ol>
  <li>Normal training images are embedded using a pretrained Vision Transformer.</li>
  <li>Test images are converted into embeddings in the same feature space.</li>
  <li>A similarity metric (Cosine/Euclidean distance) measures how different the test image is from the learned normal distribution.</li>
  <li>If the distance is above a threshold, the image is flagged as defective.</li>
</ol>

<hr>

<p>
This project highlights how <strong>self-supervised learning, deep embeddings, and similarity-based analysis</strong> can be used to build scalable industrial inspection systems with minimal labeled data.
</p>
""", unsafe_allow_html=True)
