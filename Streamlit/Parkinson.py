import streamlit as st
import pickle
import numpy as np
import time
import requests
import json
from streamlit_lottie import st_lottie

# Load the trained model
model = pickle.load(open("Parkinsons.pkl", "rb"))

# Define the Streamlit app
def main():
    st.title("🧠 Parkinson's Disease Prediction")
    st.write("Enter the following details to predict if a person has Parkinson's disease:")

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
    # Grouping inputs into columns in the specified order
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        mdvp_fo_hz = st.number_input("MDVP:Fo(Hz)", min_value=0.0, format="%.5f")
        mdvp_jitter_pct = st.number_input("MDVP:Jitter(%)", min_value=0.0, format="%.5f")
        jitter_ddp = st.number_input("Jitter:DDP", min_value=0.0, format="%.5f")
        shimmer_apq3 = st.number_input("Shimmer:APQ3", min_value=0.0, format="%.5f")
        nhr = st.number_input("NHR", min_value=0.0, format="%.5f")
        rpde = st.number_input("RPDE", min_value=0.0, format="%.5f")

    with col2:
        mdvp_fhi_hz = st.number_input("MDVP:Fhi(Hz)", min_value=0.0, format="%.5f")
        mdvp_jitter_abs = st.number_input("MDVP:Jitter(Abs)", min_value=0.0, format="%.5f")
        mdvp_shimmer = st.number_input("MDVP:Shimmer", min_value=0.0, format="%.5f")
        shimmer_apq5 = st.number_input("Shimmer:APQ5", min_value=0.0, format="%.5f")
        hnr = st.number_input("HNR", min_value=0.0, format="%.5f")
        dfa = st.number_input("DFA", min_value=0.0, format="%.5f")

    with col3:
        mdvp_flo_hz = st.number_input("MDVP:Flo(Hz)", min_value=0.0, format="%.5f")
        mdvp_rap = st.number_input("MDVP:RAP", min_value=0.0, format="%.5f")
        mdvp_shimmer_db = st.number_input("MDVP:Shimmer(dB)", min_value=0.0, format="%.5f")
        mdvp_apq = st.number_input("MDVP:APQ", min_value=0.0, format="%.5f")
        spread1 = st.number_input("Spread1", format="%.5f")
        spread2 = st.number_input("Spread2", format="%.5f")

    with col4:
        mdvp_ppq = st.number_input("MDVP:PPQ", min_value=0.0, format="%.5f")
        d2 = st.number_input("D2", min_value=0.0, format="%.5f")
        ppe = st.number_input("PPE", min_value=0.0, format="%.5f")
        shimmer_dda = st.number_input("Shimmer:DDA", min_value=0.0, format="%.5f")

    # Prediction button
    if st.button("Predict"):
        try:
            # Check if all inputs are provided
            inputs = [mdvp_fo_hz, mdvp_fhi_hz, mdvp_flo_hz, mdvp_jitter_pct,
                      mdvp_jitter_abs, mdvp_rap, mdvp_ppq, jitter_ddp,
                      mdvp_shimmer, mdvp_shimmer_db, shimmer_apq3, shimmer_apq5,
                      mdvp_apq, nhr, hnr, rpde, dfa, spread1,
                      spread2, d2, ppe, shimmer_dda]

            if any(x == 0.0 for x in inputs):
                st.error("Please ensure all input fields are filled in.")
                return

            with st.spinner("Processing..."):
                progress = st.progress(0)
                for i in range(100):
                    time.sleep(0.01)  # Simulate computation time
                    progress.progress(i + 1)

            # Prepare the input data for prediction
            input_data = np.array([inputs])

            # Make prediction
            prediction = model.predict(input_data)

            col1, col2 = st.columns([1, 2])

            if prediction[0] == 1:
                with col1:
                    lottie_hello = load_lottieurl("https://lottie.host/c8c3a923-b57e-45de-a98c-fad26640cce9/nHbTRDeXuG.json")
                    st_lottie(lottie_hello, reverse=True, height=200, width=200, speed=1, loop=True, quality='high', key="hello1")

                with col2:
                    st.markdown(
                        """
                        <div class="result-box">
                            You have Parkinson's disease.
                            <div class="subtext">Courage doesn’t always roar; sometimes it’s the quiet determination to keep going.</div>
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
                            You do not have Parkinson's disease.
                            <div class="subtext">Your journey to wellness is on the right path—keep it up!</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
        except ValueError:
            st.error("Please ensure all inputs are numeric and valid.")
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
