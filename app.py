import streamlit as st
import os

#give the folder that is to be created and where the image will be store a name 
upload_folder='uploaded_image'

#if the folder does not exist then it creates one
if not os.path.exists(upload_folder):
    os.mkdir(upload_folder)
    

# Now give heading to our website
st.header('Please upload the image below')
# Now provide the header to upload the image and box
file_uploaded=st.file_uploader("choose an image........",type=['jpg','jpeg','png'])

# check whether the file is uploaded or not and if uploaded take the file name and then create path
if file_uploaded is not None:
    file_name=file_uploaded.name
    file_path=os.path.join(upload_folder,file_name)
#     '''1. with open(file_path, 'wb') as f:

# open(file_path, 'wb'): Opens a file located at file_path.

# 'w' → write mode (creates or overwrites the file).

# 'b' → binary mode (the file is written as raw bytes, not text).

# with ... as f: ensures the file is properly closed automatically when done, even if an error occurs.

# 2. f.write(file_uploaded.getbuffer())

# file_uploaded is likely an uploaded file object (e.g., from Streamlit or Flask).

# .getbuffer() returns a memoryview object of the file’s contents (raw bytes).

# f.write(...) writes those bytes into the file at file_path.'''
    with open(file_path,'wb') as f:
        f.write(file_uploaded.getbuffer())
    st.success(f'file uploaded successfully...{file_path}')        
    st.image(file_uploaded,caption='uploaded image',use_container_width=True)