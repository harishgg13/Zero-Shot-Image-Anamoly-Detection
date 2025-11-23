import joblib
import torch
from html_css import page1_home,page1_footer
import streamlit as st

if "page" not in st.session_state:
    st.session_state.page = "Detector"

page1_home()


if "page" in st.query_params:
    st.session_state.page = st.query_params["page"]
# --------------------------------------------------------------------------------------------------------------------
import pymysql
con=pymysql.connect(
    host="localhost",        # your DB host
    user="root",             # your username
    password="12345678",
    database="production"
)
cursor = con.cursor()

# --------------------------------------------------------------------------------------------------------------------
def insertion(table_name,result,defect_type):
    query=f"insert into {table_name} (result,defect_type) values (%s,%s);"
    cursor.execute(query,(result,defect_type))
    con.commit()
# --------------------------------------------------------------------------------------------------------------------


knn_toothbrush = joblib.load("knn_toothbrush_good_model.pkl")
hazelnut_knn = joblib.load("knn_hazelnut_good_model.pkl")

from transformers import AutoImageProcessor, AutoModel
model_name = "facebook/dino-vitb8"
processor = AutoImageProcessor.from_pretrained(model_name)
encoder = AutoModel.from_pretrained(model_name)
encoder.eval()

from torchvision import transforms
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

from transformers import AutoImageProcessor, AutoModel
def get_embed_from_pil(img_pil):
    x = transform(img_pil)  # transform defined earlier
    with torch.no_grad():
        inputs = processor(images=x, return_tensors="pt", do_rescale=False)
        outputs = encoder(**inputs)
    emb = outputs.last_hidden_state[:, 0, :].squeeze(0)  # (768,)
    return emb.cpu().numpy().reshape(1, -1)

from PIL import Image
best_threshold = 16

# ----------------------------------------------------------

def toothbrush_predict_image(path):
    # load image
    img = Image.open(path).convert("RGB")
    
    # get embedding
    emb_np = get_embed_from_pil(img)   # function defined earlier
    
    # kNN distance
    dist, _ = knn_toothbrush.kneighbors(emb_np)
    score = dist.mean()

    # classification
    label = "DEFECTIVE" if score >= best_threshold else "GOOD"

    return score, label

def hazelnut_predict_image(path):
    # load image
    img = Image.open(path).convert("RGB")
    
    # get embedding
    emb_np = get_embed_from_pil(img)   # function defined earlier
    
    # kNN distance
    dist, _ = hazelnut_knn.kneighbors(emb_np)
    score = dist.mean()

    # classification
    if score < 25.1:
        label = "GOOD"

    elif 25.1 <= score < 27.5:
        label = "CUT"

    elif 27.5 <= score <= 37.5:
        label = "CUT or HOLE"    # overlap area

    elif 37.5 <= score <= 47.1:
        label = "CRACK or HOLE"    # overlap area

    elif score > 47.1:
        label = "CRACK"

    return score, label

# ----------------------------------------------------------
if st.session_state.page == "Detector":
    option = st.selectbox(
        "Choose the Product",
        ("Hazelnut","Tooth Brush"),
    )

    if option == "Tooth Brush":
        if st.button("Reset Machine",key="predict_btn1"):
            delete_query="delete from toothbrush;"
            cursor.execute(delete_query)
            con.commit()
        uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

        if uploaded_file is not None:
            score, label = toothbrush_predict_image(uploaded_file)
            st.write("### 🏷 Prediction:", label)
            # st.write("### 🏷 score:", score)
            result = 1 if label == "GOOD" else 0
            insert_data=insertion("toothbrush",result,label)
        else:
            st.write("Please upload an image to continue.")

    elif option == "Hazelnut":
        if st.button("Reset Machine",key="predict_btn2"):
            delete_query="delete from hazelnut;"
            cursor.execute(delete_query)
            con.commit()
        uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

        if uploaded_file is not None:
            score, label = hazelnut_predict_image(uploaded_file)
            st.write("### 🏷 Prediction:", label)
            # st.write("### 🏷 score:", score)
            result = 1 if label == "GOOD" else 0
            insert_data=insertion("hazelnut",result,label)
        else:
            st.write("Please upload an image to continue.")

# --------------------------------------------------------------------------------------------------------------------

if st.session_state.page == "Machine Status":
    exec(open("machine_status.py").read())

if st.session_state.page == "About":
    exec(open("About.py").read())

# --------------------------------------------------------------------------------------------------------------------
page1_footer()