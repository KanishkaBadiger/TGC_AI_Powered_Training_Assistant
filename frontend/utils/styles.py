# utils/styles.py
import streamlit as st


def load_styles():
    # Professional Modern Color Scheme CSS with White Background
    st.markdown("""
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body, html {
            background: #ffffff;
            color: #2d3142;
            font-family: 'Segoe UI', 'Trebuchet MS', sans-serif;
        }
        
        .main {
            background: #ffffff;
            color: #2d3142;
            padding: 30px;
        }
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #f0f4f8 0%, #e8ecf1 100%) !important;
        }
        
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
            color: #2d3142 !important;
        }
        
        [data-testid="stSidebar"] * {
            color: #2d3142 !important;
        }
        
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
            color: #2d3142 !important;
        }
        
        [data-testid="stSidebar"] label {
            color: #2d3142 !important;
        }
        
        /* Hide sidebar on auth pages */
        .hide-sidebar [data-testid="stSidebar"] {
            display: none !important;
        }
        
        /* Header Styles - Modern Gradient */
        .header-main {
            background: linear-gradient(135deg, #23b5d3 0%, #62929e 100%);
            padding: 60px 50px;
            border-radius: 20px;
            text-align: center;
            color: #ffffff;
            margin-bottom: 40px;
            box-shadow: 0 15px 50px rgba(35, 181, 211, 0.25);
            animation: slideDown 0.6s ease-out;
            border: none;
        }
        
        .header-main h1 {
            font-size: 3.5rem;
            font-weight: 900;
            margin-bottom: 15px;
            text-shadow: 0 2px 8px rgba(0,0,0,0.2);
            color: #ffffff;
            letter-spacing: -0.5px;
        }
        
        .header-main p {
            font-size: 1.3rem;
            opacity: 0.95;
            font-weight: 500;
            color: #ffffff;
            letter-spacing: 0.5px;
        }
        
        /* Professional Card Styles */
        .card {
            background: linear-gradient(135deg, #e8f4f8 0%, #f0f8fc 100%);
            border: 2px solid #23b5d3;
            border-left: 6px solid #ef8354;
            border-radius: 12px;
            padding: 25px;
            margin: 15px 0;
            box-shadow: 0 6px 20px rgba(35, 181, 211, 0.15);
            transition: all 0.3s cubic-bezier(0.4, 0.0, 0.2, 1);
        }
        
        .card:hover {
            border-left-color: #23b5d3;
            border-color: #ef8354;
            box-shadow: 0 15px 35px rgba(239, 131, 84, 0.2);
            transform: translateY(-6px);
        }
        
        .card-title {
            font-size: 1.4rem;
            font-weight: 700;
            color: #2d3142;
            margin-bottom: 10px;
            border-bottom: 2px solid #23b5d3;
            padding-bottom: 10px;
        }
        
        /* Feature Cards - Modern Grid */
        .feature-card {
            background: linear-gradient(135deg, #ffffff 0%, #f0f9fb 100%);
            border: 2px solid #23b5d3;
            border-radius: 15px;
            padding: 30px;
            text-align: center;
            transition: all 0.3s ease;
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }
        
        .feature-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 5px;
            background: linear-gradient(90deg, #ef8354, #23b5d3, #62929e);
        }
        
        .feature-card:hover {
            border-color: #23b5d3;
            box-shadow: 0 15px 40px rgba(35, 181, 211, 0.2);
            transform: translateY(-8px);
        }
        
        .feature-icon {
            font-size: 3.5rem;
            margin-bottom: 15px;
            animation: bounce 2s infinite;
        }
        
        .feature-name {
            font-size: 1.3rem;
            font-weight: 700;
            color: #2d3142;
            margin-bottom: 10px;
        }
        
        .feature-desc {
            font-size: 0.95rem;
            color: #4f5d75;
            line-height: 1.6;
        }
        
        /* Project Info Cards */
        .info-card {
            background: linear-gradient(135deg, #fef5f1 0%, #fef9f5 100%);
            border-left: 6px solid #ef8354;
            border-radius: 10px;
            padding: 20px;
            margin: 12px 0;
            transition: all 0.3s ease;
            border-top: 2px solid #23b5d3;
        }
        
        .info-card:hover {
            border-left-color: #23b5d3;
            background: linear-gradient(135deg, #fffaf8 0%, #ffffff 100%);
            box-shadow: 0 10px 25px rgba(239, 131, 84, 0.2);
            transform: translateX(8px);
        }
        
        .info-card-title {
            font-size: 1.1rem;
            font-weight: 700;
            color: #23b5d3;
            margin-bottom: 8px;
        }
        
        .info-card-desc {
            font-size: 0.95rem;
            color: #4f5d75;
            line-height: 1.6;
        }
        
        /* Button Styles - Premium */
        .stButton > button {
            background: linear-gradient(135deg, #ef8354 0%, #e07040 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 12px 32px !important;
            font-weight: 700 !important;
            font-size: 1rem !important;
            transition: all 0.3s ease !important;
            text-transform: uppercase !important;
            letter-spacing: 0.5px !important;
            box-shadow: 0 8px 20px rgba(239, 131, 84, 0.3) !important;
        }
        
        .stButton > button:hover {
            box-shadow: 0 15px 35px rgba(239, 131, 84, 0.5) !important;
            transform: translateY(-3px) !important;
            background: linear-gradient(135deg, #f09060 0%, #e85c3c 100%) !important;
        }
        
        /* Input Styles */
        .stTextInput > div > div > input,
        .stPasswordInput > div > div > input,
        .stSelectbox > div > div > select,
        .stTextArea > div > div > textarea,
        .stNumberInput > div > div > input {
            background: #ffffff !important;
            border: 2px solid #e0e0e0 !important;
            color: #2d3142 !important;
            border-radius: 10px !important;
            padding: 12px 15px !important;
            font-size: 1rem !important;
            transition: all 0.3s ease !important;
        }
        
        .stTextInput > div > div > input:focus,
        .stPasswordInput > div > div > input:focus,
        .stSelectbox > div > div > select:focus,
        .stTextArea > div > div > textarea:focus,
        .stNumberInput > div > div > input:focus {
            border-color: #23b5d3 !important;
            box-shadow: 0 0 0 3px rgba(35, 181, 211, 0.1) !important;
            background: #ffffff !important;
        }
        
        /* Metrics - Modern Cards */
        .stMetric {
            background: linear-gradient(135deg, #ffffff 0%, #f5f7fa 100%) !important;
            border: 2px solid #e0e0e0 !important;
            border-top: 4px solid #23b5d3 !important;
            padding: 25px !important;
            border-radius: 12px !important;
            transition: all 0.3s ease !important;
        }
        
        .stMetric:hover {
            border-top-color: #ef8354 !important;
            transform: translateY(-5px) !important;
            box-shadow: 0 12px 30px rgba(35, 181, 211, 0.15) !important;
        }
        
        /* Messages */
        .stSuccess {
            background: #e8f5e9 !important;
            border-left: 4px solid #4caf50 !important;
            border-radius: 8px !important;
            padding: 15px !important;
            color: #2d3142 !important;
        }
        
        .stError {
            background: #ffebee !important;
            border-left: 4px solid #ef8354 !important;
            border-radius: 8px !important;
            padding: 15px !important;
            color: #2d3142 !important;
        }
        
        .stWarning {
            background: #fff3e0 !important;
            border-left: 4px solid #ff9800 !important;
            border-radius: 8px !important;
            padding: 15px !important;
            color: #2d3142 !important;
        }
        
        .stInfo {
            background: #e1f5fe !important;
            border-left: 4px solid #23b5d3 !important;
            border-radius: 8px !important;
            padding: 15px !important;
            color: #2d3142 !important;
        }
        
        /* Animations */
        @keyframes slideDown {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-15px); }
        }
        
        /* Divider */
        hr {
            border: none;
            height: 2px;
            background: linear-gradient(90deg, transparent, #e0e0e0, transparent);
            margin: 30px 0;
        }
        
        h2 { 
            color: #2d3142 !important; 
            border-bottom: 3px solid #23b5d3; 
            padding-bottom: 10px; 
            font-weight: 800 !important;
            font-size: 2rem !important;
        }
        
        h3 { 
            color: #23b5d3 !important; 
            font-weight: 700 !important;
            font-size: 1.5rem !important;
        }
        
        h4 { 
            color: #62929e !important; 
            font-weight: 600 !important;
        }
        
        p { 
            color: #4f5d75;
            line-height: 1.7;
        }
        
        /* Sidebar Radio Button Styling */
        [data-testid="stSidebar"] .stRadio > label {
            color: #ffffff !important;
            font-weight: 600 !important;
        }
        
        [data-testid="stSidebar"] .stRadio > div {
            gap: 15px !important;
        }
    </style>
    """, unsafe_allow_html=True)
