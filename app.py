import streamlit as st
from PIL import Image, ExifTags

# Helper: convert rational numbers safely
def rational_to_float(rational):
    try:
        if isinstance(rational, tuple) and len(rational) == 2:
            num, den = rational
            return num / den if den != 0 else 0
        return float(rational)
    except Exception:
        return 0

# Helper: convert DMS to decimal degrees
def dms_to_decimal(dms, ref):
    degrees = rational_to_float(dms[0])
    minutes = rational_to_float(dms[1])
    seconds = rational_to_float(dms[2])
    decimal = degrees + minutes/60 + seconds/3600
    if ref in ['S', 'W']:
        decimal = -decimal
    return decimal

# Extract full EXIF metadata including GPS
def extract_metadata(image):
    exif_data = {}
    gps_info = {}

    if hasattr(image, "_getexif") and image._getexif():
        raw_exif = image._getexif()
        for tag, value in raw_exif.items():
            tag_name = ExifTags.TAGS.get(tag, tag)
            exif_data[tag_name] = value

        # Parse GPSInfo if available
        if "GPSInfo" in exif_data:
            gps_raw = exif_data["GPSInfo"]
            for key in gps_raw.keys():
                gps_tag = ExifTags.GPSTAGS.get(key, key)
                gps_info[gps_tag] = gps_raw[key]

            # Convert to decimal coordinates if possible
            if "GPSLatitude" in gps_info and "GPSLongitude" in gps_info:
                lat = dms_to_decimal(gps_info["GPSLatitude"], gps_info.get("GPSLatitudeRef", "N"))
                lon = dms_to_decimal(gps_info["GPSLongitude"], gps_info.get("GPSLongitudeRef", "E"))
                gps_info["DecimalCoordinates"] = (lat, lon)

    return exif_data, gps_info

# Streamlit UI
st.title("📸 Detailed Image Metadata Viewer")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png", "tiff", "heic"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    image = Image.open(uploaded_file)

    exif_data, gps_info = extract_metadata(image)

    # Show all EXIF metadata
    if exif_data:
        st.subheader("Full EXIF Metadata")
        for key, value in exif_data.items():
            st.markdown(f"**{key}:** {value}")
    else:
        st.warning("No EXIF metadata found.")

    # Show GPS info
    if gps_info:
        st.subheader("GPS Information")
        for key, value in gps_info.items():
            st.markdown(f"**{key}:** {value}")
        if "DecimalCoordinates" in gps_info:
            lat, lon = gps_info["DecimalCoordinates"]
            st.success(f"📍 Coordinates: {lat}, {lon}")
    else:
        st.info("No GPS data found in this image.")
