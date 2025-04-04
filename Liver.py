import streamlit as st
import numpy as np
import pickle
import requests
import json
import time
from streamlit_lottie import st_lottie

model = pickle.load(open("Liver.pkl", "rb"))
def main():
    def load_lottieurl(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    
    page_bg_img = '''
<style>
[data-testid="stAppViewContainer"] {
    background-image: url(https://img.freepik.com/free-vector/clean-medical-background_53876-97927.jpg?t=st=1735554505~exp=1735558105~hmac=e7124c3ad0fd8f58e6491a225d2ade8eb911413cea15dd1a9a40884dc85b722b&w=996);
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}

[data-testid="stMarkdownContainer"]{
background-color: rgba(0,0,0,0);
color: blue;

</style>
    '''
    st.markdown(
    """
    <style>
    .result-box {
        background: linear-gradient(to right, #6a11cb, #2575fc);
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
        text-align: center;
        color: white;
        font-family: 'Arial', sans-serif;
        font-size: 24px;
        font-weight: bold;
    }
    .subtext {
        font-size: 18px;
        font-weight: normal;
        margin-top: 10px;
        color: #f0f0f0;
    }
    </style>
    """,
    unsafe_allow_html=True
)
    st.markdown(page_bg_img, unsafe_allow_html=True)

    def predict_liver_disease(age, gender, total_bilirubin, direct_bilirubin, alkaline_phosphotase,
                          alamine_aminotransferase, aspartate_aminotransferase, total_proteins,
                          albumin, albumin_and_globulin_ratio):
            gender_encoded = 1 if gender.lower() == 'male' else 0

    
            input_data = np.array([[age, gender_encoded, total_bilirubin, direct_bilirubin, 
                             alkaline_phosphotase, alamine_aminotransferase, 
                             aspartate_aminotransferase, total_proteins, albumin, 
                             albumin_and_globulin_ratio]])

    # Make the prediction
            prediction = model.predict(input_data)
            return prediction[0]
    
    st.title("🩸Indian Liver Disease Prediction ")
    st.write("Enter the required details below to predict Indian Liver Disease.")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
         age = st.number_input("Age", min_value=1, max_value=120, value=None)
    with col2:
        gender = st.selectbox("Gender", ["", "Male", "Female"])  # Initial empty value for gender
    with col3:
        total_bilirubin = st.number_input("Total Bilirubin", value=None)
    with col4:
        direct_bilirubin = st.number_input("Direct Bilirubin", value=None)
    with col5:
        alkaline_phosphotase = st.number_input("Alkaline Phosphotase", value=None)

    col6, col7, col8, col9, col10 = st.columns(5)

    with col6:
        alamine_aminotransferase = st.number_input("Alamine Aminotransferase", value=None)
    with col7:
        aspartate_aminotransferase = st.number_input("Aspartate Aminotransferase", value=None)
    with col8:
        total_proteins = st.number_input("Total Proteins", value=None)
    with col9:
        albumin = st.number_input("Albumin", value=None)
    with col10:
        albumin_and_globulin_ratio = st.number_input("Albumin and Globulin Ratio", value=None)

    if st.button("Predict"):
        if None in [age, gender, total_bilirubin, direct_bilirubin, alkaline_phosphotase, 
                alamine_aminotransferase, aspartate_aminotransferase, total_proteins, 
                albumin, albumin_and_globulin_ratio] or gender == "":
             st.error("Please fill in all the fields.")
        else:
            prediction = predict_liver_disease(age, gender, total_bilirubin, direct_bilirubin, 
                                           alkaline_phosphotase, alamine_aminotransferase, 
                                           aspartate_aminotransferase, total_proteins, 
                                           albumin, albumin_and_globulin_ratio)
            with st.spinner("Processing..."):
                progress = st.progress(0)
                for i in range(100):
                    time.sleep(0.01)  # Simulate computation time
                    progress.progress(i + 1)

            col1, col2 = st.columns([1, 2])
            
            if prediction == 2:
                with col1:
                    
                    
                    lottie_hello = load_lottieurl("https://lottie.host/c8c3a923-b57e-45de-a98c-fad26640cce9/nHbTRDeXuG.json")
                    st_lottie(lottie_hello, reverse=True, height=200, width=200, speed=1, loop=True, quality='high', key="hello1")

                with col2:
                    st.markdown(
                        """
                        <div class="result-box">
                            You  have Liver Disease (LD).
                            <div class="subtext">Diagnosis is not the end, but the beginning of a new fight. You’ve got this!</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                
            else:
                with col1:
                    lottie_hello = load_lottieurl("https://lottie.host/1deb01b3-28f9-4d2d-976c-bb7b83f58ad7/IyQoBSol6A.json")
                    st_lottie(lottie_hello, reverse=True, height=200, width=200, speed=1, loop=True, quality='high', key="hello2")
                    
                    
                with col2:
                    st.markdown(
                        """
                        <div class="result-box">
                            You donot have Liver disease(LD).
                            <div class="subtext">Health is the greatest gift; today, you've unwrapped yours.</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

if __name__ == "__main__":
    main()