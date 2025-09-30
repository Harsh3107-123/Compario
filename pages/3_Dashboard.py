import streamlit as st
from PIL import Image


st.set_page_config(page_title="Image Upload with Size Limit", page_icon="🖼️", layout="wide")
st.title("Image Upload with Size Limit")

backend = st.sidebar.selectbox(
    "Backend",
    options=["Hugging Face ViT (ImageNet)", "TorchVision ResNet-50 (ImageNet)"],
    index=0,
)
top_k = st.sidebar.slider("Top-K predictions", min_value=1, max_value=5, value=3)

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"], accept_multiple_files=False)

if uploaded_file is None:
    st.info("Upload an image to begin.")
else:
    st.caption("Maximum file size: 5 MB")
    from image_processing import is_within_size_limit, load_pil_rgb
    if not is_within_size_limit(uploaded_file, max_mb=5.0):
        st.error("File size exceeds 5 MB. Please upload a smaller image.")
    else:
        image = load_pil_rgb(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        if backend == "Hugging Face ViT (ImageNet)":
            try:
                from recognition import classify_with_hf
                with st.spinner("Identifying (Hugging Face ViT)..."):
                    rows = classify_with_hf(image, top_k=top_k)
                for item in rows:
                    label, prob = item
                    st.write(f"{label}: {prob:.2%}")
                    st.progress(min(max(prob, 0.0), 1.0))
            except Exception:
                st.error("Hugging Face pipeline failed. Ensure transformers is installed.")

        else:  # TorchVision ResNet-50
            try:
                from recognition import classify_with_torchvision
                with st.spinner("Identifying (TorchVision ResNet-50)..."):
                    rows = classify_with_torchvision(image, top_k=top_k)
                for label, prob in rows:
                    st.write(f"{label}: {prob:.2%}")
                    st.progress(min(max(prob, 0.0), 1.0))
            except Exception:
                st.error("TorchVision inference failed. Ensure torch and torchvision are installed.")

