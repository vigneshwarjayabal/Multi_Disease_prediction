import streamlit as st
import numpy as np
import pickle
import requests
import json
import time
from streamlit_lottie import st_lottie

model = pickle.load(open("Kidney.pkl", "rb"))
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



    categorical_mapping = {
    "rbc": {"normal": 1, "abnormal": 0},
    "pc": {"normal": 1, "abnormal": 0},
    "pcc": {"notpresent": 0, "present": 1},
    "ba": {"notpresent": 0, "present": 1},
    "htn": {"yes": 1, "no": 0},
    "dm": {"yes": 1, "no": 0},
    "cad": {"yes": 1, "no": 0},
    "appet": {"good": 1, "poor": 0},
    "pe": {"yes": 1, "no": 0},
    "ane": {"yes": 1, "no": 0},
}

    def handle_missing_values(value):
        if value is None or value == "":
            return 0.0  
        try:
            return float(value)
        except ValueError:
            return 0.0  


    def predict_kidney_disease(features):
        prediction = model.predict(features)
        return prediction

    st.title("🩺 Kidney Disease Prediction ")
    st.write("Enter the following details to predict if a person has kidney disease:")
    for row in range(6):
        cols = st.columns(4)
    
        if row == 0:
            with cols[0]:
                age = st.number_input("Age", min_value=0, max_value=300, step=1, value=0)
            with cols[1]:
                bp = st.number_input("Blood Pressure (BP)", min_value=0, max_value=500, step=1, value=0)
            with cols[2]:
                sg = st.number_input("Specific Gravity (SG)", min_value=1.000, max_value=2.030, step=0.001, format="%.3f", value=1.000)
            with cols[3]:
                al = st.number_input("Albumin (AL)", min_value=0, max_value=10, step=1, value=0)

        elif row == 1:
            with cols[0]:
                su = st.number_input("Sugar (SU)", min_value=0, max_value=10, step=1, value=0)
            with cols[1]:
                rbc = st.selectbox("Red Blood Cells (RBC)", ["", "normal", "abnormal"])
            with cols[2]:
                pc = st.selectbox("Pus Cell (PC)", ["", "normal", "abnormal"])
            with cols[3]:
                pcc = st.selectbox("Pus Cell Clumps (PCC)", ["", "notpresent", "present"])

        elif row == 2:
            with cols[0]:
                ba = st.selectbox("Bacteria (BA)", ["", "notpresent", "present"])
            with cols[1]:
                bgr = st.number_input("Blood Glucose Random (BGR)", min_value=0, max_value=700, step=1, value=0)
            with cols[2]:
                bu = st.number_input("Blood Urea (BU)", min_value=0, max_value=500, step=1, value=0)
            with cols[3]:
                sc = st.number_input("Serum Creatinine (SC)", min_value=0.0, max_value=50.0, step=0.1, value=0.0)

        elif row == 3:
            with cols[0]:
                sod = st.number_input("Sodium (SOD)", min_value=0, max_value=500, step=1, value=0)
            with cols[1]:
                pot = st.number_input("Potassium (POT)", min_value=0.0, max_value=30.0, step=0.1, value=0.0)
            with cols[2]:
                hemo = st.number_input("Hemoglobin (HEMO)", min_value=0.0, max_value=50.0, step=0.1, value=0.0)
            with cols[3]:
                pcv = st.text_input("Packed Cell Volume (PCV)", value="0")

        elif row == 4:
            with cols[0]:
                wc = st.text_input("White Blood Cell Count (WC)", value="0")
            with cols[1]:
                rc = st.text_input("Red Blood Cell Count (RC)", value="0")
            with cols[2]:
                htn = st.selectbox("Hypertension (HTN)", ["", "yes", "no"])
            with cols[3]:
                dm = st.selectbox("Diabetes Mellitus (DM)", ["", "yes", "no"])

        elif row == 5:
            with cols[0]:
                cad = st.selectbox("Coronary Artery Disease (CAD)", ["", "yes", "no"])
            with cols[1]:
                appet = st.selectbox("Appetite", ["", "good", "poor"])
            with cols[2]:
                pe = st.selectbox("Pedal Edema (PE)", ["", "yes", "no"])
            with cols[3]:
                ane = st.selectbox("Anemia (ANE)", ["", "yes", "no"])

    if st.button("Predict"):
        try:
            pcv = handle_missing_values(pcv)
            wc = handle_missing_values(wc)
            rc = handle_missing_values(rc)

        # Validate inputs
            if "" in [rbc, pc, pcc, ba, htn, dm, cad, appet, pe, ane]:
                st.error("Please fill in all the fields.")
            else:
            # Prepare the feature array for prediction
                features = np.array([[ 
                age, bp, sg, al, su, 
                categorical_mapping["rbc"].get(rbc, 0), 
                categorical_mapping["pc"].get(pc, 0), 
                categorical_mapping["pcc"].get(pcc, 0), 
                categorical_mapping["ba"].get(ba, 0), 
                bgr, bu, sc, sod, pot, hemo, 
                pcv, wc, rc,
                categorical_mapping["htn"].get(htn, 0), 
                categorical_mapping["dm"].get(dm, 0), 
                categorical_mapping["cad"].get(cad, 0), 
                categorical_mapping["appet"].get(appet, 0), 
                categorical_mapping["pe"].get(pe, 0), 
                categorical_mapping["ane"].get(ane, 0)
            ]])

            
            features = features.reshape(1, -1)

           
            prediction = predict_kidney_disease(features)
            with st.spinner("Processing..."):
                progress = st.progress(0)
                for i in range(100):
                    time.sleep(0.01)  # Simulate computation time
                    progress.progress(i + 1)

            col1, col2 = st.columns([1, 2])

            
            if prediction == 1:
                with col1:
                    
                    lottie_hello = load_lottieurl("https://lottie.host/1deb01b3-28f9-4d2d-976c-bb7b83f58ad7/IyQoBSol6A.json")
                    st_lottie(lottie_hello, reverse=True, height=200, width=200, speed=1, loop=True, quality='high', key="hello2")

                with col2:
                    st.markdown(
                        """
                        <div class="result-box">
                            You donot have Chronic Kidney Disease (CKD).
                            <div class="subtext">A healthy mind and body are your greatest treasures. Cherish them.</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                
            else:
                with col1:
                    lottie_hello = load_lottieurl("https://lottie.host/c8c3a923-b57e-45de-a98c-fad26640cce9/nHbTRDeXuG.json")
                    st_lottie(lottie_hello, reverse=True, height=200, width=200, speed=1, loop=True, quality='high', key="hello1")
                    
                with col2:
                    st.markdown(
                        """
                        <div class="result-box">
                            You  have Chronic Kidney disease(CKD).
                            <div class="subtext">This is a chapter, not the whole story. You're stronger than you know</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

        except ValueError as ve:
            st.error(f"ValueError encountered: {ve}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()

