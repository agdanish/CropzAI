import streamlit as st

# UI Setup
st.set_page_config(
    page_title="CropzAI - Multi-Agent Advisor", 
    page_icon="🌱", 
    layout="wide",
    initial_sidebar_state="expanded"
)

from dotenv import load_dotenv
import os

load_dotenv()  # ✅ This loads the .env file

# Now this will work:
api_token = os.getenv("HF_API_TOKEN")

from io import BytesIO
import importlib
import os
import uuid
import sqlite3
from datetime import datetime
import pandas as pd
from ollama import Client
import time
from streamlit_lottie import st_lottie
import requests
import json
from streamlit_option_menu import option_menu
import streamlit_authenticator as stauth
import base64
from utilities.llm_wrappers import OllamaWrapper, HuggingFaceWrapper

import os
import requests

def is_ollama_running():
    try:
        r = requests.get("http://localhost:11434")
        return r.status_code == 200
    except:
        return False

def get_llm():
    if is_ollama_running():
        return OllamaWrapper(model_name="llama3")
    else:
        return HuggingFaceWrapper(
            model_url="https://api-inference.huggingface.co/models/gpt2",
            api_token=os.getenv("HF_API_TOKEN")
        )

# Function to load image as base64 for background
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

import base64
import streamlit as st
import os
import requests
from io import BytesIO

def set_image_as_page_bg(path_or_url):
    try:
        if path_or_url.startswith("http"):
            # Remote image
            response = requests.get(path_or_url)
            if response.status_code == 200:
                image_data = response.content
                ext = os.path.splitext(path_or_url)[-1].lower()
            else:
                raise ValueError("Could not fetch image from URL.")
        else:
            # Local file
            with open(path_or_url, "rb") as f:
                image_data = f.read()
            ext = os.path.splitext(path_or_url)[-1].lower()

        mime_type = "image/jpeg" if ext in [".jpg", ".jpeg"] else "image/png"
        bin_str = base64.b64encode(image_data).decode()

        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:{mime_type};base64,{bin_str}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

    except Exception as e:
        print("Error loading background image:", e)
        # Optional fallback
        st.markdown(
            """
            <style>
            .stApp {
                background: linear-gradient(135deg, #e0f7fa 0%, #f5f7fa 100%);
                background-attachment: fixed;
            }
            </style>
            """,
            unsafe_allow_html=True
        )


# Alternative function to create a gradient background
def set_gradient_background():
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(to bottom right, #e0f7ea, #c8e6c9, #a5d6a7);
            background-attachment: fixed;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Custom CSS for styling
def load_css():
    st.markdown("""
    <style>
    /* Glass morphism effect for containers */
    .glass-container {
        background: rgba(255, 255, 255, 0.75);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.17);
        padding: 20px;
        margin-bottom: 20px;
    }
    
    /* Make form elements pop more */
    .stSelectbox, .stSlider, .stTextInput, .stNumberInput {
        background-color: white;
        border-radius: 8px;
        padding: 5px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }
    
    /* Style tabs better */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background-color: rgba(255, 255, 255, 0.7);
        border-radius: 15px;
        padding: 5px;
        margin-bottom: 15px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #3a86ff !important;
        color: white !important;
        box-shadow: 0 4px 10px rgba(58, 134, 255, 0.3);
    }
    
    /* Style buttons */
    .stButton>button {
        background: linear-gradient(90deg, #3a86ff, #4361ee);
        color: white;
        border-radius: 10px;
        padding: 12px 24px;
        font-weight: 600;
        border: none;
        transition: all 0.3s;
        box-shadow: 0 4px 15px rgba(74, 97, 238, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 7px 15px rgba(74, 97, 238, 0.4);
    }
    
    /* Style expandable sections */
    div[data-testid="stExpander"] {
        border: 1px solid rgba(255, 255, 255, 0.5);
        border-radius: 10px;
        margin-bottom: 15px;
        background-color: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        transition: all 0.3s;
    }
    
    div[data-testid="stExpander"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.08);
    }
    
    /* Style agent cards */
    .agent-card {
        padding: 20px;
        border-radius: 15px;
        background-color: rgba(255, 255, 255, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        transition: all 0.4s ease;
    }
    
    .agent-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.08);
    }
    
    /* Style metrics */
    [data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.7);
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        transition: transform 0.3s ease;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    /* Style report sections */
    .report-header {
        background: linear-gradient(90deg, #3a86ff, #4361ee);
        color: white;
        padding: 15px;
        border-radius: 10px 10px 0 0;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(74, 97, 238, 0.2);
    }
    
    .report-body {
        padding: 20px;
        background-color: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 0 0 10px 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    
    /* Style sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.5);
    }
    
    /* Style main content headers */
    h1, h2, h3 {
        color: #1a3a6c;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    /* Add animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.6s ease-out forwards;
    }
    
    .delay-1 {
        animation-delay: 0.2s;
    }
    
    .delay-2 {
        animation-delay: 0.4s;
    }
    
    .delay-3 {
        animation-delay: 0.6s;
    }
    
    /* Cards animation */
    @keyframes pop {
        0% { transform: scale(0.95); opacity: 0.8; }
        100% { transform: scale(1); opacity: 1; }
    }
    
    .pop-in {
        animation: pop 0.4s ease-out forwards;
    }
    
    /* Notification pulse animation */
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(58, 134, 255, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(58, 134, 255, 0); }
        100% { box-shadow: 0 0 0 0 rgba(58, 134, 255, 0); }
    }
    
    .pulse {
        animation: pulse 2s infinite;
    }
    
    /* Make text more readable on transparent backgrounds */
    p, li, label, span {
        text-shadow: 0 0 2px rgba(255,255,255,0.8);
    }
    
    /* Progress bar styling */
    [data-testid="stProgressBar"] {
        background-color: rgba(255, 255, 255, 0.3);
        border-radius: 10px;
        height: 10px !important;
    }
    
    [data-testid="stProgressBar"] > div {
        background: linear-gradient(90deg, #3a86ff, #4361ee) !important;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

import streamlit.components.v1 as components

particles_html = """
<div id="particles-js" style="position: fixed; width: 100%; height: 100%; z-index: -1;"></div>
<script src="https://cdn.jsdelivr.net/npm/particles.js"></script>
<script>
particlesJS('particles-js',
{
  "particles": {
    "number": {
      "value": 30,
      "density": {
        "enable": true,
        "value_area": 800
      }
    },
    "color": {
      "value": "#3a86ff"
    },
    "shape": {
      "type": "circle"
    },
    "opacity": {
      "value": 0.3,
      "random": true,
      "anim": {
        "enable": true,
        "speed": 0.5,
        "opacity_min": 0.1,
        "sync": false
      }
    },
    "size": {
      "value": 5,
      "random": true,
      "anim": {
        "enable": true,
        "speed": 1,
        "size_min": 0.1,
        "sync": false
      }
    },
    "line_linked": {
      "enable": true,
      "distance": 150,
      "color": "#3a86ff",
      "opacity": 0.2,
      "width": 1
    },
    "move": {
      "enable": true,
      "speed": 1,
      "random": true,
      "straight": false,
      "out_mode": "out",
      "bounce": false
    }
  },
  "interactivity": {
    "events": {
      "onhover": {
        "enable": true,
        "mode": "grab"
      },
      "onclick": {
        "enable": true,
        "mode": "push"
      },
      "resize": true
    },
    "modes": {
      "grab": {
        "distance": 140,
        "line_linked": {
          "opacity": 0.8
        }
      },
      "push": {
        "particles_nb": 3
      }
    }
  },
  "retina_detect": true
});
</script>
"""

components.html(particles_html, height=0, width=0)

# Function to load Lottie animations
def load_lottie_url(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Function to create a spinning loading animation
def loading_spinner():
    with st.spinner('Processing your data...'):
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress_bar.progress(i + 1)
        st.success('Analysis complete!')
        time.sleep(0.5)
        progress_bar.empty()

# Particles configuration for animated background
def configure_particles():
    particles_config = {
        "particles": {
            "number": {
                "value": 30,
                "density": {
                    "enable": True,
                    "value_area": 800
                }
            },
            "color": {
                "value": "#3a86ff"
            },
            "shape": {
                "type": "circle",
                "stroke": {
                    "width": 0,
                    "color": "#000000"
                },
            },
            "opacity": {
                "value": 0.3,
                "random": True,
                "anim": {
                    "enable": True,
                    "speed": 0.5,
                    "opacity_min": 0.1,
                    "sync": False
                }
            },
            "size": {
                "value": 5,
                "random": True,
                "anim": {
                    "enable": True,
                    "speed": 1,
                    "size_min": 0.1,
                    "sync": False
                }
            },
            "line_linked": {
                "enable": True,
                "distance": 150,
                "color": "#3a86ff",
                "opacity": 0.2,
                "width": 1
            },
            "move": {
                "enable": True,
                "speed": 1,
                "direction": "none",
                "random": True,
                "straight": False,
                "out_mode": "out",
                "bounce": False,
            }
        },
        "interactivity": {
            "detect_on": "canvas",
            "events": {
                "onhover": {
                    "enable": True,
                    "mode": "grab"
                },
                "onclick": {
                    "enable": True,
                    "mode": "push"
                },
                "resize": True
            },
            "modes": {
                "grab": {
                    "distance": 140,
                    "line_linked": {
                        "opacity": 0.8
                    }
                },
                "push": {
                    "particles_nb": 3
                }
            }
        },
        "retina_detect": True
    }
    return particles_config

# Load datasets
@st.cache_data
def load_data():
    try:
        market_df = pd.read_csv("https://raw.githubusercontent.com/agdanish/CropzAI/main/2.%20Datasets/market_researcher_dataset.csv")
        farmer_df = pd.read_csv("https://raw.githubusercontent.com/agdanish/CropzAI/main/2.%20Datasets/farmer_advisor_dataset.csv")
        return market_df, farmer_df
    except Exception as e:
        st.warning(f"Using sample data due to error: {str(e)}")
        # Create sample data
        market_df = pd.DataFrame({
            "Product": ["Wheat", "Rice", "Corn", "Soybean", "Cotton"],
            "Price": [2500, 3000, 1800, 2200, 4500],
            "Demand": [80, 90, 70, 75, 65]
        })
        
        farmer_df = pd.DataFrame({
            "Crop_Type": ["Wheat", "Rice", "Corn", "Soybean", "Cotton"],
            "Region": ["North", "South", "East", "West", "Central"],
            "Yield": [5.2, 4.8, 6.1, 3.9, 2.7]
        })
        
        return market_df, farmer_df

try:
    market_df, farmer_df = load_data()
    
    # Dropdown values
    crop_types = sorted(farmer_df["Crop_Type"].dropna().unique())
    products = sorted(market_df["Product"].dropna().unique())
    regions = sorted(farmer_df["Region"].dropna().unique()) if "Region" in farmer_df.columns else ["Your Farm"]
except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    crop_types = ["Wheat", "Rice", "Corn", "Soybean", "Cotton"]
    products = ["Grain", "Vegetable", "Fruit", "Fiber"]
    regions = ["North", "South", "East", "West", "Central"]

# Setup DB and LLM
db_conn = sqlite3.connect(r"D:\CropzAI\4. Database\cropzai_memory.db", check_same_thread=False)
llm = get_llm()

# Load agents
AGENT_DIR = "agents"
AGENT_LIST = [
    "CropKnowledge", "PriceMonitor", "DemandTrend", "SupplyAnalytics", "CompetitorMarket",
    "Economy", "Climate", "Season", "Consumer", "Soil", "Irrigation", "Temperature",
    "Rainfall", "CropHistory", "Fertilizer", "Pesticide", "Yield", "SoilMoisture",
    "WeatherImpact", "RegionAdvisor", "BudgetPlanner", "SmartSustainability", "WaterAdvisor",
    "MarketForecaster", "LanguageAgent"
]

agents = {}
for name in AGENT_LIST:
    try:
        mod = importlib.import_module(f"{AGENT_DIR}.{name}")
        cls = getattr(mod, name)
        agents[name] = cls(db_conn=db_conn, llm=llm)
    except Exception as e:
        st.warning(f"Could not load agent {name}: {str(e)}")

# Try to set background image, fall back to gradient
try:
    # If you have an image file, uncomment the line below:
    set_image_as_page_bg("https://images.unsplash.com/photo-1606788075761-7c56c2dc6635")

    # If not, use a gradient:
    #set_gradient_background()
except:
    set_gradient_background()

# Load custom CSS
load_css()

# Create animated particle background
particles_config = configure_particles()

# Sidebar with navigation
from PIL import Image  # Add this to your imports if not already included

with st.sidebar:
    # Lottie animation for sidebar
    farming_animation = load_lottie_url("https://assets9.lottiefiles.com/packages/lf20_agovjzpu.json")
    if farming_animation:
        st_lottie(farming_animation, speed=1, height=200, key="farming_anim")

    st.markdown('<div class="glass-container">', unsafe_allow_html=True)

    # Load and display logo
    try:
        logo_url = "https://raw.githubusercontent.com/agdanish/CropzAI/main/3.%20Utilities/cropzai_logo.png"
        logo = Image.open(BytesIO(requests.get(logo_url).content))
        st.image(logo, width=180)  # Adjust width as needed
    except Exception as e:
        st.warning(f"Logo not found: {e}")

    # App name and subtitle
    st.title("🌱 CropzAI")
    st.subheader("Sustainable Farming Advisor")

    st.markdown('</div>', unsafe_allow_html=True)

    
    with st.container():
        st.markdown('<div class="glass-container">', unsafe_allow_html=True)
        selected = option_menu(
            menu_title=None,
            options=["Dashboard", "Analysis", "History", "About"],
            icons=["house", "graph-up", "clock-history", "info-circle"],
            default_index=1,
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "icon": {"color": "#3a86ff", "font-size": "18px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "rgba(255,255,255,0.7)",
                },
                "nav-link-selected": {"background-color": "#3a86ff"},
            }
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown("### Latest Updates")
    st.markdown('<div class="pulse">', unsafe_allow_html=True)
    st.info("🆕 New climate predictions available")
    st.markdown('</div>', unsafe_allow_html=True)
    st.info("🔄 Market prices updated today")
    st.markdown('</div>', unsafe_allow_html=True)

# Main content
if selected == "Dashboard":
    st.markdown('<div class="fade-in glass-container">', unsafe_allow_html=True)
    # Dashboard view 
    st.title("🌱 CropzAI Dashboard")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Weather animation
    weather_animation = load_lottie_url("https://assets9.lottiefiles.com/packages/lf20_XkF78Y.json")
    if weather_animation:
        st.markdown('<div class="fade-in delay-1">', unsafe_allow_html=True)
        st_lottie(weather_animation, speed=1, height=250, key="weather_anim")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="fade-in delay-2 glass-container">', unsafe_allow_html=True)
    st.subheader("Quick Overview")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="pop-in">', unsafe_allow_html=True)
        st.metric(label="Temperature", value="30 °C", delta="2 °C")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="pop-in">', unsafe_allow_html=True)
        st.metric(label="Rainfall", value="100 mm", delta="-10 mm")
        st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="pop-in">', unsafe_allow_html=True)
        st.metric(label="Market Price", value="₹2500/ton", delta="₹100")
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="fade-in delay-3 glass-container">', unsafe_allow_html=True)
    st.subheader("Recent Reports")
    st.write("No recent reports. Run a new analysis to see results here.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Market trends animation
    market_animation = load_lottie_url("https://assets8.lottiefiles.com/packages/lf20_doyhajlm.json")
    if market_animation:
        st.markdown('<div class="fade-in delay-3">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st_lottie(market_animation, speed=1, height=250, key="market_anim")
        st.markdown('</div>', unsafe_allow_html=True)

elif selected == "Analysis":
    st.markdown('<div class="fade-in glass-container">', unsafe_allow_html=True)
    st.title("🌱 CropzAI Analysis")
    st.markdown("### Multi-Agent Sustainable Farming Advisor")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Nice animation for the analysis page
    farming_tech_animation = load_lottie_url("https://assets8.lottiefiles.com/private_files/lf30_8bj1vhqx.json")
    if farming_tech_animation:
        st.markdown('<div class="fade-in delay-1">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st_lottie(farming_tech_animation, speed=1, height=250, key="farming_tech_anim")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Create tabs for better organization
    st.markdown('<div class="fade-in delay-2">', unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["📝 Input Parameters", "📊 Analysis Results"])
    st.markdown('</div>', unsafe_allow_html=True)
    
    with tab1:
        st.markdown('<div class="glass-container">', unsafe_allow_html=True)
        with st.form("multi_agent_input"):
            st.subheader("Enter Your Farming Parameters")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("##### Crop Information")
                crop_type = st.selectbox("Crop Type", crop_types, help="Select the type of crop you are growing")
                soil_ph = st.number_input("Soil pH", value=6.5, min_value=0.0, max_value=14.0, 
                                        help="The pH level of your soil, typically 6-7 is ideal for most crops")
                temp = st.number_input("Temperature (°C)", value=30, min_value=-10, max_value=50, 
                                    help="Average temperature in your region")
                rainfall = st.number_input("Rainfall (mm)", value=100, min_value=0, 
                                        help="Average monthly rainfall in your region")
            
            with col2:
                st.markdown("##### Farm Management")
                region = st.selectbox("Region", regions, help="Your farming region")
                soil_moisture = st.number_input("Soil Moisture (%)", value=20, min_value=0, max_value=100, 
                                            help="Current soil moisture percentage")
                fertilizer_kg = st.number_input("Fertilizer Usage (kg/acre)", value=50, min_value=0, 
                                            help="Amount of fertilizer used per acre")
                pesticide_kg = st.number_input("Pesticide Usage (kg/acre)", value=10, min_value=0, 
                                            help="Amount of pesticide used per acre")
            
            with col3:
                st.markdown("##### Market Factors")
                yield_ton = st.number_input("Crop Yield (ton/acre)", value=5.0, min_value=0.0, 
                                        help="Expected crop yield per acre")
                product = st.selectbox("Market Product", products, help="The final product you're selling")
                market_price = st.number_input("Market Price (₹/ton)", value=2500, min_value=0, 
                                            help="Current market price per ton")
                competitor_price = st.number_input("Competitor Price (₹/ton)", value=2400, min_value=0, 
                                                help="Average competitor price per ton")
            
            st.markdown("##### Market Indicators")
            col1, col2 = st.columns(2)
            
            with col1:
                demand_index = st.slider("Demand Index", 0, 100, 60, 
                                        help="Current market demand (higher is stronger demand)")
                supply_index = st.slider("Supply Index", 0, 100, 50, 
                                        help="Current market supply (higher is more supply)")
                consumer_trend = st.slider("Consumer Trend Index", 0, 100, 70, 
                                        help="Consumer preference trend (higher is more favorable)")
            
            with col2:
                seasonal_factor = st.slider("Seasonal Factor", 0, 100, 60, 
                                        help="Seasonal impact on market (higher is more favorable)")
                economic_indicator = st.slider("Economic Indicator", 0, 100, 50, 
                                            help="General economic health (higher is better economy)")
                language = st.selectbox("Preferred Language", 
                                    ["English", "Hindi", "Tamil", "Telugu", "Kannada", "Bengali"])
            
            submitted = st.form_submit_button("Run Multi-Agent Analysis")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        if submitted:
            # Animate loading
            loading_spinner()
            
            session_id = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
            input_data = {
                "Crop_Type": crop_type,
                "Soil_pH": soil_ph,
                "Temperature_C": temp,
                "Rainfall_mm": rainfall,
                "Soil_Moisture": soil_moisture,
                "Fertilizer_Usage_kg": fertilizer_kg,
                "Pesticide_Usage_kg": pesticide_kg,
                "Crop_Yield_ton": yield_ton,
                "Region": region,
                "Product": product,
                "Market_Price_per_ton": market_price,
                "Competitor_Price_per_ton": competitor_price,
                "Demand_Index": demand_index,
                "Supply_Index": supply_index,
                "Consumer_Trend_Index": consumer_trend,
                "Seasonal_Factor": seasonal_factor,
                "Economic_Indicator": economic_indicator
            }
            
            # Log user session
            db_conn.execute("""
                CREATE TABLE IF NOT EXISTS user_sessions (
                    session_id TEXT PRIMARY KEY,
                    input_data TEXT,
                    timestamp TEXT
                )
            """)
            db_conn.execute(
                "INSERT INTO user_sessions (session_id, input_data, timestamp) VALUES (?, ?, ?)",
                (session_id, str(input_data), datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            )
            db_conn.commit()
            
            # Display summary card
            st.markdown('<div class="fade-in">', unsafe_allow_html=True)
            st.markdown("<div class='report-header'>Multi-Agent Analysis Summary</div>", unsafe_allow_html=True)
            st.markdown("<div class='report-body'>", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown('<div class="pop-in">', unsafe_allow_html=True)
                st.metric("Crop", crop_type)
                st.metric("Region", region)
                st.markdown('</div>', unsafe_allow_html=True)
            with col2:
                st.markdown('<div class="pop-in">', unsafe_allow_html=True)
                st.metric("Market Price", f"₹{market_price}/ton")
                st.metric("Expected Yield", f"{yield_ton} ton/acre")
                st.markdown('</div>', unsafe_allow_html=True)
            with col3:
                st.markdown('<div class="pop-in">', unsafe_allow_html=True)
                st.metric("Demand", f"{demand_index}%")
                st.metric("Supply", f"{supply_index}%")
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("---")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Create agent groups for better organization
            agent_groups = {
                "Market Analysis": ["PriceMonitor", "DemandTrend", "SupplyAnalytics", "CompetitorMarket", "Economy", "Consumer", "MarketForecaster"],
                "Crop Management": ["CropKnowledge", "Soil", "Fertilizer", "Pesticide", "Yield", "CropHistory"],
                "Environmental Factors": ["Climate", "Temperature", "Rainfall", "Irrigation", "SoilMoisture", "WeatherImpact", "WaterAdvisor"],
                "Planning & Regional": ["Season", "RegionAdvisor", "BudgetPlanner", "SmartSustainability"],
            }
            
            # Keep LanguageAgent separate as it's applied to all outputs
            if "LanguageAgent" in agents:
                language_agent = agents.pop("LanguageAgent")
            else:
                language_agent = None
            
            # Process and display agents by group
            delay_counter = 0
            for group_name, agent_names in agent_groups.items():
                delay_class = f"delay-{delay_counter % 3 + 1}"
                st.markdown(f'<div class="fade-in {delay_class} glass-container">', unsafe_allow_html=True)
                st.subheader(f"📊 {group_name}")
                cols = st.columns(2)
                col_idx = 0
                
                for name in agent_names:
                    if name in agents:
                        try:
                            with st.spinner(f"Running {name} analysis..."):
                                output = agents[name].analyze(input_data, session_id=session_id)
                                
                                # Apply language translation if needed
                                if language != "English" and language_agent:
                                    with st.spinner(f"Translating to {language}..."):
                                        output = language_agent.analyze({"output_text": output, "language": language}, session_id=session_id)
                                
                                with cols[col_idx]:
                                    card_delay = (col_idx + 1) % 3
                                    st.markdown(f'<div class="pop-in delay-{card_delay}">', unsafe_allow_html=True)
                                    with st.expander(f"🔹 {name}", expanded=False):
                                        st.markdown(f"<div class='agent-card'>{output}</div>", unsafe_allow_html=True)
                                    st.markdown('</div>', unsafe_allow_html=True)
                                
                                # Alternate between columns
                                col_idx = (col_idx + 1) % 2
                                
                        except Exception as e:
                            with cols[col_idx]:
                                with st.expander(f"🔻 {name} (Error)", expanded=False):
                                    st.error(str(e))
                            col_idx = (col_idx + 1) % 2
                st.markdown('</div>', unsafe_allow_html=True)
                delay_counter += 1
        else:
            st.markdown('<div class="glass-container">', unsafe_allow_html=True)
            st.info("👆 Submit the form to see analysis results here")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Show a placeholder animation when no results are available
            analysis_animation = load_lottie_url("https://assets3.lottiefiles.com/packages/lf20_qp1q7mct.json")
            if analysis_animation:
                st.markdown('<div class="fade-in delay-1">', unsafe_allow_html=True)
                col1, col2, col3 = st.columns([1,2,1])
                with col2:
                    st_lottie(analysis_animation, speed=1, height=300, key="analysis_anim")
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Show sample insights to give an idea
            st.markdown('<div class="fade-in delay-2 glass-container">', unsafe_allow_html=True)
            st.subheader("Sample Insights Preview")
            sample_cols = st.columns(2)
            
            with sample_cols[0]:
                st.markdown('<div class="agent-card">', unsafe_allow_html=True)
                st.markdown("#### 🌾 Crop Knowledge")
                st.markdown("""
                Wheat requires moderate temperatures (15-24°C) and annual rainfall of 750-1600mm.
                Ideal soil pH: 6.0-7.0. Planting depth: 3-5cm.
                
                Fill the form and analyze for personalized insights!
                """)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with sample_cols[1]:
                st.markdown('<div class="agent-card">', unsafe_allow_html=True)
                st.markdown("#### 💧 Water Advisor")
                st.markdown("""
                Efficient irrigation scheduling can reduce water usage by 30-50%.
                
                Input your farm details for customized water management recommendations!
                """)
                st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

elif selected == "History":
    st.markdown('<div class="fade-in glass-container">', unsafe_allow_html=True)
    st.title("📜 Analysis History")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # History animation
    history_animation = load_lottie_url("https://assets4.lottiefiles.com/packages/lf20_GpHzXd.json")
    if history_animation:
        st.markdown('<div class="fade-in delay-1">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st_lottie(history_animation, speed=1, height=200, key="history_anim")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="fade-in delay-2 glass-container">', unsafe_allow_html=True)
    try:
        # Fetch history from database
        cursor = db_conn.execute("SELECT session_id, timestamp FROM user_sessions ORDER BY timestamp DESC LIMIT 10")
        sessions = cursor.fetchall()
        
        if sessions:
            st.subheader("Recent Analysis Sessions")
            for i, (session_id, timestamp) in enumerate(sessions):
                delay = i % 3
                st.markdown(f'<div class="pop-in delay-{delay}">', unsafe_allow_html=True)
                with st.expander(f"Session: {timestamp}"):
                    st.code(session_id, language="text")
                    st.button(f"Load Session {i+1}", key=f"load_{session_id}")
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No analysis history found. Run your first analysis to see it here.")
    except Exception as e:
        st.error(f"Error fetching history: {str(e)}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Calendar view animation
    calendar_animation = load_lottie_url("https://assets1.lottiefiles.com/packages/lf20_rjgbjue3.json")
    if calendar_animation:
        st.markdown('<div class="fade-in delay-3">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st_lottie(calendar_animation, speed=1, height=200, key="calendar_anim")
        st.markdown('</div>', unsafe_allow_html=True)

elif selected == "About":
    st.markdown('<div class="fade-in glass-container">', unsafe_allow_html=True)
    st.title("ℹ️ About CropzAI")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # About animation
    about_animation = load_lottie_url("https://assets2.lottiefiles.com/private_files/lf30_crfxcqey.json")
    if about_animation:
        st.markdown('<div class="fade-in delay-1">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st_lottie(about_animation, speed=1, height=300, key="about_anim")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="fade-in delay-2 glass-container">', unsafe_allow_html=True)
    st.markdown("""
    ### Multi-Agent Sustainable Farming Advisor
    
    CropzAI is an advanced farming advisory system that uses multiple AI agents to provide 
    comprehensive analysis and recommendations for sustainable farming practices.
    
    #### Features:
    - 🌾 Crop-specific recommendations
    - 📊 Market analysis and price predictions
    - 🌦️ Weather impact assessment
    - 💧 Water and irrigation optimization
    - 💲 Budget planning and cost optimization
    - 🌍 Region-specific advice
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="fade-in delay-3 glass-container">', unsafe_allow_html=True)
    st.markdown("""
    #### How It Works:
    Our system uses multiple specialized AI agents, each focusing on different aspects of 
    farming and market analysis. These agents work together to provide you with comprehensive
    insights tailored to your specific farming conditions and market environment.
    
    Each agent analyzes your data from a different perspective:
    
    - **Market Agents** evaluate prices, demand, supply, and economic factors
    - **Crop Agents** focus on optimal growth conditions and yield improvement
    - **Environmental Agents** analyze climate, water needs, and sustainability
    - **Planning Agents** help optimize resources and long-term strategy
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Team animation
    team_animation = load_lottie_url("https://assets3.lottiefiles.com/packages/lf20_eofrbqcl.json")
    if team_animation:
        st.markdown('<div class="fade-in delay-3">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st_lottie(team_animation, speed=1, height=200, key="team_anim")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="fade-in delay-3 glass-container">', unsafe_allow_html=True)
    st.markdown("""
    #### Contact Information
    📧 Email: danish@xzashr.com  
    📱 Phone: +91-8903099026 
    🌐 Website: www.xzashr.com
    
    #### Version
    CropzAI v1.2.0
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: rgba(255,255,255,0.8); padding: 10px; 
        background-color: rgba(0,0,0,0.2); border-radius: 10px; backdrop-filter: blur(5px);
        margin-top: 30px;">
        CropzAI © 2025 | Sustainable Farming Solutions
    </div>
    """, 
    unsafe_allow_html=True
)

# Add the necessary dependencies to requirements.txt for this app
# pip install streamlit streamlit-lottie streamlit-option-menu streamlit-particles streamlit-authenticator
