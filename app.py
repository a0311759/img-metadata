import streamlit as st
from PIL import Image, ExifTags

# Title
st.title("📸 Image Metadata Viewer")

# File uploader
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png", "heic", "tiff"])

def get_exif_data(image):
    exif_data = {}
    if hasattr(image, "_getexif") and image._getexif():
        for tag, value in image._getexif().items():
            tag_name = ExifTags.TAGS.get(tag, tag)
            exif_data[tag_name] = value
    return exif_data

if uploaded_file is not None:
    # Display image
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

    # Open image with Pillow
    image = Image.open(uploaded_file)

    # Extract metadata
    exif_data = get_exif_data(image)

    if exif_data:
        st.subheader("Metadata Extracted:")
        # Render metadata as HTML-like table
        for key, value in exif_data.items():
            st.markdown(f"**{key}:** {value}")
    else:
        st.warning("No EXIF metadata found in this image.")
