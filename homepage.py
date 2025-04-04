import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import requests
import json

st.set_page_config (
    page_title="Home Page",
    page_icon=None,
)

page_bg_img = '''
<style>
[data-testid="stAppViewContainer"] {
    background-image: url(https://img.freepik.com/free-vector/clean-medical-background_53876-97927.jpg?t=st=1735554505~exp=1735558105~hmac=e7124c3ad0fd8f58e6491a225d2ade8eb911413cea15dd1a9a40884dc85b722b&w=996);
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}

[data-testid="stHeadingWithActionElements"]{
background-color: rgba(0,0,0,0);
color: black;
}

[data-testid="stMarkdownContainer"]{
background-color: rgba(0,0,0,0);
color: black;
}
</style>

'''

st.markdown(page_bg_img, unsafe_allow_html=True)
select = option_menu (
        menu_title=None,
        options=["Home","Parkinsons","Kidney","Liver"],
        icons=["house","activity", "droplet", "heart"],
        orientation= "horizontal",
    )
col1, col2 = st.columns([3,1])

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_hello = load_lottieurl("https://lottie.host/ef4e927b-fb21-4ed7-ab38-280ec82cdd08/o3vREHgBEV.json")
if select == "Home":
    with col2:
        st_lottie(lottie_hello,reverse=True,height=200,width=200,speed=1,loop=True,quality='high',key="hello")

    with col1:
        st.title('🔖 MULTI DISEASE PREDICTION')
        st.subheader("Welcome to Your Health Ally")
        st.subheader("Empowering Early Detection, One Click at a Time")
        st.write(
    '''
At the heart of your well-being lies timely care and accurate insights. Our Multi-Disease Prediction App is your trusted companion in health, designed to empower you with advanced AI-driven diagnostics for Parkinson's Disease, Liver Disease, and Kidney Disease.

🌟 Why Choose Us?

🎖️ Fast & Reliable Predictions: Get accurate health insights in just seconds.
🎖️ User-Friendly Interface: Simplified for everyone—no technical expertise required!

🎖️ Secure & Confidential: Your health data is protected with state-of-the-art encryption.

🧠 Parkinson's Disease
Detect early signs of Parkinson's to seek timely medical guidance and improve quality of life.

🩸 Liver Disease
Analyze key indicators and uncover potential liver health risks for proactive care.

💧 Kidney Disease
Monitor vital parameters to identify early warning signs and prevent complications.


How It Works


1) Enter the required health parameters.
2) Let our advanced algorithms process your data.
3) Receive detailed predictions and actionable advice.

✨ Your health journey matters, and we’re here to make it smarter, simpler, and safer. Start today—because prevention is always better than cure!
'''
)

elif select == "Parkinsons":
    import Parkinson
    Parkinson.main()
elif select == "Kidney":
    import Kidney
    Kidney.main()
elif select == "Liver":
    import Liver
    Liver.main()
