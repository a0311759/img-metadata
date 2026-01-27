import streamlit as st
from PIL import Image, ExifTags

st.title("📸 Image Metadata Viewer")

uploaded_file = st.file_uploader(
    "Upload an image",
    type=["jpg", "jpeg", "png", "tiff"]
)

def get_exif_data(image):
    exif_data = {}
    exif = image.getexif()
    if exif:
        for tag_id, value in exif.items():
            tag = ExifTags.TAGS.get(tag_id, tag_id)
            exif_data[tag] = value
    return exif_data

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    exif_data = get_exif_data(image)

    if exif_data:
        st.subheader("Metadata Extracted:")
        for k, v in exif_data.items():
            st.markdown(f"**{k}:** {v}")
    else:
        st.warning("No EXIF metadata found.")
        
