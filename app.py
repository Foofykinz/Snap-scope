import streamlit as st
from PIL import Image
import os
import datetime
import io

st.set_page_config(page_title="SnapScope™", layout="centered")
st.title("📸 SnapScope™ – Guided Photo Capture")

# Your part checklist
part_list = [
    "Dash VIN", "Door VIN", "LF Corner", "RF Corner",
    "RR Corner", "LR Corner", "Odometer", "Dash",
    "Headliner", "LF Seat", "LF Carpet", "LF Door Trim"
]

# Session state setup
if "index" not in st.session_state:
    st.session_state.index = 0
if "photos_taken" not in st.session_state:
    st.session_state.photos_taken = {}

# Unit identifier input
st.subheader("📦 Set Unit/Folder Name (e.g., VIN, Plate)")
unit_id = st.text_input("Unit ID:", value=st.session_state.get("unit_id", ""))
st.session_state.unit_id = unit_id.strip()

# Folder name generator
today = datetime.date.today().strftime("%Y-%m-%d")
base_folder = f"SnapScope_{today}_{unit_id}" if unit_id else f"SnapScope_{today}"
st.code(f"📁 Save location: labeled_photos/{base_folder}/")

# If all photos done
if st.session_state.index >= len(part_list):
    st.success("✅ All required photos have been captured and labeled.")
    st.stop()

# Current photo step
current_part = part_list[st.session_state.index]
filename = f"{st.session_state.index + 1:02d}_{current_part.replace(' ', '_')}.jpg"

st.markdown(f"### 📷 Take a photo of: **{current_part}**")
st.caption(f"💾 It will be saved as: `{filename}`")

# Upload vs camera input toggle
upload_method = st.radio("Choose input method:", ["📁 Upload", "📷 Use Camera"])

file = None
if upload_method == "📁 Upload":
    file = st.file_uploader("Upload photo", type=["jpg", "jpeg", "png"], key=current_part)
else:
    file = st.camera_input("Capture photo with your camera", key=current_part)

# Save photo
if file:
    image = Image.open(file)
    st.image(image, caption=current_part, use_container_width=True)

    if st.button("✅ Save and Continue"):
        folder_path = os.path.join("labeled_photos", base_folder, current_part.replace(" ", "_"))
        os.makedirs(folder_path, exist_ok=True)

        full_path = os.path.join(folder_path, filename)
        with open(full_path, "wb") as f:
            f.write(file.getbuffer())

        st.success(f"Saved to: {full_path}")
        st.session_state.index += 1
        st.rerun()

# Back/skip buttons
col1, col2 = st.columns(2)
if col1.button("⏮️ Back", disabled=st.session_state.index == 0):
    st.session_state.index = max(0, st.session_state.index - 1)
    st.rerun()

if col2.button("⏭️ Skip"):
    st.session_state.index += 1
    st.rerun()

