import streamlit as st
import pandas as pd




st.set_page_config(
    page_title="Unit Converter", 
    page_icon="🔄", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

if "dark_mode" not in st.session_state:
    st.session_state["dark_mode"] = False
if "history" not in st.session_state:
    st.session_state["history"] = []
if "show_history" not in st.session_state:
    st.session_state["show_history"] = False

st.session_state["dark_mode"] = st.sidebar.checkbox("🌙 Dark Mode", st.session_state["dark_mode"])


if st.session_state["dark_mode"]:
    background_color = "#121212"
    text_color = "#ffffff"
    result_bg = "#1e1e2f"
    success_color = "#00ff00"
else:
    background_color = "#ffffff"
    text_color = "#000000"
    result_bg = "#f0f0f0"
    success_color = "#008000"

st.markdown(
    f"""
    <style>
    body {{ 
        background-color: {background_color}; 
        color: {text_color}; 
        }}
        
    .stApp {{ 
        padding: 20px; 
        border-radius: 15px; 
        box-shadow: 0px 10px 30px rgba(0,0,0,0.3); 
        background: {background_color}; 
        color: {text_color}; 
        }}

    h1, h4 {{ 
        text-align: center; 
        color: #00c9ff; 
        }}

    .result-box {{ 
        font-size: 24px; 
        text-align: center; 
        background: {result_bg}; 
        padding: 15px; 
        border-radius: 10px; 
        color: #00c9ff; 
        margin-top: 20px; 
        }}

    .footer {{ 
        text-align: center; 
        margin-top: 50px; 
        font-size: 18px; 
        color: {text_color}; 
        }}

    .history-box {{ 
        font-size: 16px; 
        padding: 10px; 
        border-radius: 5px; 
        background: {result_bg}; 
        margin-top: 10px; 
        border-left: 5px solid #00c9ff; 
        padding-left: 10px; 
        }}

    .success-message {{ 
        font-size: 18px; 
        text-align: center; 
        color: {success_color}; 
        margin-top: 10px; 
        font-weight: extrabold; 
        }}

    .stButton>button {{
        background: linear-gradient(45deg, #0b5394, #351c75);
        color: white;
        font-size: 18px;
        padding: 10px 20px;
        border-radius: 10px;
        transition: 0.3s;
        box-shadow: 0px 5px 15px rgba(0,201,255,0.4);
        font-weight: extrabold;
        border: none;
        cursor: pointer;
        }}

    .stButton>button:hover {{
        transform: scale(1.05);
        background: linear-gradient(45deg, #92fe9d, #00c9ff);
        color: black;
        font-weight: extrabold;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1> 🔄 Unit Converter</h1>", unsafe_allow_html=True)

st.write("<h4>Easily Convert Between Various Units</h4>", unsafe_allow_html=True)

conversion_type = st.sidebar.selectbox("Select Conversion Type", ["Length", "Weight", "Temperature", "Speed", "Time", "Volume", "Pressure"])

col1, col2 = st.columns(2)

with col1:
    value = st.number_input("Enter Value", value=0.0, step=0.1, min_value=0.0)

unit_options = {
    "Length": ["Meter", "Kilometer", "Centimeter", "Millimeter", "Mile", "Yard", "Feet", "Inches"],
    "Weight": ["Kilogram", "Gram", "Milligram", "Pound", "Ounce"],
    "Temperature": ["Celsius", "Fahrenheit", "Kelvin"],
    "Speed": ["km/h", "mph", "m/s"],
    "Time": ["Seconds", "Minutes", "Hours", "Days"],
    "Volume": ["Liters", "Milliliters", "Cubic Meters", "Gallons"],
    "Pressure": ["Pascal", "Bar", "PSI", "Atmosphere"]
}

col3, col4 = st.columns(2)

with col3:
    from_unit = st.selectbox("From Unit", unit_options[conversion_type])

with col4:
    to_unit = st.selectbox("To Unit", unit_options[conversion_type])

def convert(value, from_unit, to_unit):
        conversions = {
            "Length": {"Meter": 1, "Kilometer": 0.001, "Centimeter": 100, "Millimeter": 1000, "Mile": 0.000621371, "Yard": 1.09361, "Feet": 3.28084, "Inches": 39.3701},
            "Weight": {"Kilogram": 1, "Gram": 1000, "Milligram": 1e6, "Pound": 2.20462, "Ounce": 35.274},
            "Speed": {"km/h": 1, "mph": 0.621371, "m/s": 0.277778},
            "Time": {"Seconds": 1, "Minutes": 1/60, "Hours": 1/3600, "Days": 1/86400},
            "Volume": {"Liters": 1, "Milliliters": 1000, "Cubic Meters": 0.001, "Gallons": 0.264172},
            "Pressure": {"Pascal": 1, "Bar": 1e-5, "PSI": 0.000145038, "Atmosphere": 9.86923e-6}
        }

        return value * conversions[conversion_type][from_unit] / conversions[conversion_type][to_unit]

if st.button("Convert"):
    result = convert(value, from_unit, to_unit)
    conversion_text = f"{value} {from_unit} = {result:.4f} {to_unit}"
    st.session_state["history"].append(conversion_text)
    st.markdown(f"<div class='result-box'>{conversion_text}</div>", unsafe_allow_html=True)
    st.success("Conversion Successfull! ✅")

if st.button("Show History"):
    st.session_state["show_history"] = not st.session_state["show_history"]

if st.session_state["show_history"]:
    st.write("### Conversion History")

    for i, entry in enumerate(st.session_state["history"][-5:][::-1], 1):
        st.markdown(f"<div class='history-box'>{i}. {entry}</div>", unsafe_allow_html=True)
        
    if st.button("Clear History"):
        st.session_state["history"] = []
        st.markdown("<div class='success-message'> History Cleared! ✅</div>", unsafe_allow_html=True)

if st.button("Download History as CSV"):
    df = pd.DataFrame(st.session_state["history"], columns=["Conversions"])
    st.download_button("Download CSV", df.to_csv(index=False).encode("utf-8"), "conversion_history.csv", "text/csv")
    st.success("Download Successful! ✅")

st.markdown("<div class='footer'>Created By Abdul Rehman</div>", unsafe_allow_html=Tru