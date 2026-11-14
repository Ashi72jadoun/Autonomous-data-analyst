import base64
import io
import os
from graph_agent import app_graph
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from streamlit_mic_recorder import speech_to_text

# 1. Page Configuration
st.set_page_config(page_title="Aura BI Agent", page_icon="✨", layout="wide")


def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception:
        return ""


def generate_pdf(df):
    """Generates a PDF table from a DataFrame using Matplotlib"""
    fig, ax = plt.subplots(figsize=(10, min(10, len(df) * 0.5 + 1)))
    ax.axis("tight")
    ax.axis("off")
    table = ax.table(
        cellText=df.values, colLabels=df.columns, cellLoc="center", loc="center"
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.5)

    buf = io.BytesIO()
    plt.savefig(buf, format="pdf", bbox_inches="tight", transparent=True)
    plt.close(fig)
    return buf.getvalue()


bg_img_base64 = get_base64_image("Screenshot 2026-10-18 211407.png")

# 2. Theme Toggle Placement
col_spacer, col_toggle = st.columns([9.3, 0.7])
with col_toggle:
    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
    is_dark = st.toggle("Theme", value=True, label_visibility="collapsed")

# 3. Dynamic Theme Variables
if is_dark:
    bg_rgba = "rgba(35, 35, 35, 0.95)"
    main_text = "#E2E8F0"
    title_grad = "#FFFFFF, #B0BEC5"
    sub_text = "#A0AEC0"
    btn_bg = "#424242"
    btn_txt = "white"
    btn_border = "#616161"
    btn_hover = "#616161"
    input_bg = "#F8F9FA"
    input_border = "#555555"
    table_th_bg = "rgba(0,0,0,0.15)"
    table_th_text = "#000000"
    table_td_border = "rgba(0,0,0,0.1)"

    track_color = "#2B3038"
    track_border = "2px solid #E2E8F0"
    track_shadow = (
        "inset 0 2px 5px rgba(0,0,0,0.65), 0 2px 6px rgba(0,0,0,0.35)"
    )
    thumb_color = "#FFFFFF"
    thumb_shadow = "0 2px 5px rgba(0,0,0,0.45)"
    thumb_pos = "28px"
    # Crescent Moon + Stars SVG matching the 2nd image
    thumb_svg = "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none'%3E%3Cpath d='M19.5 14.5A7.5 7.5 0 0 1 9.5 4.5a7.5 7.5 0 1 0 10 10z' stroke='%237B8794' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3Cpath d='M15 4.5L15.6 6.4L17.5 7L15.6 7.6L15 9.5L14.4 7.6L12.5 7L14.4 6.4L15 4.5Z' fill='%237B8794'/%3E%3Cpath d='M19 8.5L19.4 9.6L20.5 10L19.4 10.4L19 11.5L18.6 10.4L17.5 10L18.6 9.6L19 8.5Z' fill='%237B8794'/%3E%3C/svg%3E\")"
    mic_btn_bg = "transparent"
    mic_btn_hover = "rgba(0,0,0,0.1)"
else:
    bg_rgba = "rgba(240, 244, 248, 0.95)"
    main_text = "#1A202C"
    title_grad = "#1A202C, #4A5568"
    sub_text = "#4A5568"
    btn_bg = "#FFFFFF"
    btn_txt = "#1A202C"
    btn_border = "#CBD5E1"
    btn_hover = "#F1F5F9"
    input_bg = "#FFFFFF"
    input_border = "#CBD5E1"
    table_th_bg = "rgba(255,255,255,0.5)"
    table_th_text = "#1A202C"
    table_td_border = "rgba(0,0,0,0.05)"

    track_color = "#E8ECEF"
    track_border = "2px solid #FFFFFF"
    track_shadow = (
        "inset 0 2px 5px rgba(0,0,0,0.15), 0 2px 6px rgba(0,0,0,0.10)"
    )
    thumb_color = "#FFFFFF"
    thumb_shadow = "0 2px 5px rgba(0,0,0,0.22)"
    thumb_pos = "0px"
    # Sun with 8 Rays SVG matching the 2nd image
    thumb_svg = "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%237B8794' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='12' cy='12' r='4.5'/%3E%3Cline x1='12' y1='2.5' x2='12' y2='5'/%3E%3Cline x1='12' y1='19' x2='12' y2='21.5'/%3E%3Cline x1='4.22' y1='4.22' x2='5.99' y2='5.99'/%3E%3Cline x1='18.01' y1='18.01' x2='19.78' y2='19.78'/%3E%3Cline x1='2.5' y1='12' x2='5' y2='12'/%3E%3Cline x1='19' y1='12' x2='21.5' y2='12'/%3E%3Cline x1='4.22' y1='19.78' x2='5.99' y2='18.01'/%3E%3Cline x1='18.01' y1='5.99' x2='19.78' y2='4.22'/%3E%3C/svg%3E\")"
    mic_btn_bg = "transparent"
    mic_btn_hover = "rgba(0,0,0,0.05)"

# 4. Ultra-Premium Dynamic CSS
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: linear-gradient({bg_rgba}, {bg_rgba}), url("data:image/png;base64,{bg_img_base64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        transition: background-image 0.4s ease-in-out;
    }}
    
    html, body, h1, h2, h3, p {{ color: {main_text} !important; transition: color 0.3s ease-in-out; }}
    
    /* Fix 1: Light/Dark Toggle with Sun & Moon+Stars SVG inside circular thumb */
    div[data-testid="stCheckbox"] label,
    div[data-testid="stToggle"] label,
    label:has(input[type="checkbox"]) {{
        padding: 0 !important;
        margin: 0 !important;
    }}

    div[data-testid="stCheckbox"] label > :not(input):not([data-testid="stWidgetLabel"]),
    div[data-testid="stToggle"] label > :not(input):not([data-testid="stWidgetLabel"]),
    label:has(input[type="checkbox"]) > :not(input):not([data-testid="stWidgetLabel"]) {{
        width: 60px !important;
        height: 32px !important;
        min-width: 60px !important;
        max-width: 60px !important;
        background: {track_color} !important;
        background-color: {track_color} !important;
        border: {track_border} !important;
        box-shadow: {track_shadow} !important;
        border-radius: 32px !important;
        position: relative !important;
        padding: 3px !important;
        box-sizing: border-box !important;
        display: flex !important;
        align-items: center !important;
        transition: background 0.3s ease, border 0.3s ease !important;
    }}
    
    div[data-testid="stCheckbox"] label > :not(input):not([data-testid="stWidgetLabel"]) > *,
    div[data-testid="stToggle"] label > :not(input):not([data-testid="stWidgetLabel"]) > *,
    label:has(input[type="checkbox"]) > :not(input):not([data-testid="stWidgetLabel"]) > * {{
        width: 22px !important;
        height: 22px !important;
        min-width: 22px !important;
        min-height: 22px !important;
        background-color: {thumb_color} !important;
        background-image: {thumb_svg} !important;
        background-repeat: no-repeat !important;
        background-position: center !important;
        background-size: 15px 15px !important;
        box-shadow: {thumb_shadow} !important;
        border-radius: 50% !important;
        position: relative !important;
        top: 0 !important;
        left: 0 !important;
        margin: 0 !important;
        transform: translateX({thumb_pos}) !important;
        transition: transform 0.35s cubic-bezier(0.175, 0.885, 0.32, 1.275), background-image 0.3s ease !important;
    }}
    
    /* Fix 2: Remove "Press Enter to apply" instruction inside text input */
    div[data-testid="InputInstructions"] {{
        display: none !important;
    }}
    
    .center-title {{
        text-align: center;
        font-size: 5rem;
        font-weight: 900;
        letter-spacing: 12px;
        background: -webkit-linear-gradient(45deg, {title_grad});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
        text-shadow: 0px 4px 20px rgba(0, 0, 0, 0.1);
    }}
    
    .center-subtitle {{
        text-align: center;
        font-size: 1.2rem;
        color: {sub_text} !important;
        letter-spacing: 4px;
        text-transform: uppercase;
        font-weight: 600;
        margin-top: -10px;
        margin-bottom: 40px;
    }}
    
    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stTextInput"]) {{
        background-color: {input_bg} !important;
        border: 2px solid {input_border} !important;
        border-radius: 28px !important;
        padding: 4px 14px !important;
        align-items: center !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15) !important;
        gap: 4px !important;
    }}
    
    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stTextInput"]) div[data-testid="stTextInput"] > div,
    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stTextInput"]) div[data-testid="stTextInput"] > div > div,
    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stTextInput"]) input {{
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
        color: #1A202C !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        height: 44px !important;
        padding-left: 8px !important;
        padding-right: 8px !important;
    }}

    /* Fix 3: Clear Cross Icon Column - Hidden when input is empty, shown immediately when 1+ char is typed */
    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stTextInput"]):has(input:placeholder-shown) div[data-testid="stColumn"]:nth-child(2) {{
        display: none !important;
    }}

    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stTextInput"]):has(input:not(:placeholder-shown)) div[data-testid="stColumn"]:nth-child(2) {{
        min-width: 44px !important;
        max-width: 48px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: flex-end !important;
    }}

    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stTextInput"]) div[data-testid="stColumn"]:last-child {{
        min-width: 48px !important;
        max-width: 52px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: flex-end !important;
    }}

    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stTextInput"]) iframe {{
        width: 44px !important;
        height: 40px !important;
        min-height: 40px !important;
        max-height: 40px !important;
        border: none !important;
        background: transparent !important;
        display: block !important;
        margin: 0 !important;
    }}

    button[kind="primary"], .stDownloadButton>button {{
        background: {btn_bg} !important;
        color: {btn_txt} !important;
        border-radius: 10px;
        font-weight: bold;
        font-size: 1.1rem !important;
        width: 100%;
        border: 1px solid {btn_border} !important;
        transition: 0.3s;
    }}
    button[kind="primary"]:hover, .stDownloadButton>button:hover {{
        background: {btn_hover} !important;
        border-color: {btn_border} !important;
        transform: translateY(-2px);
    }}
    
    button[kind="secondary"] {{
        background: linear-gradient(135deg, #FFBF00, #D9463E) !important;
        border: none !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3) !important;
        color: #1A1D20 !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
        text-align: left !important;
        height: auto !important;
        min-height: 80px !important;
        padding: 15px !important;
        white-space: normal !important; 
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    button[kind="secondary"]:hover {{
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.5) !important;
        color: #000000 !important;
    }}

    /* Style the Clear Cross Button to match the Mic Button exactly */
    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stTextInput"]) button[kind="secondary"] {{
        background: #FFFFFF !important;
        color: #555867 !important;
        border: 1px solid rgba(49, 51, 63, 0.2) !important;
        border-radius: 8px !important;
        width: 42px !important;
        height: 38px !important;
        min-height: 38px !important;
        max-height: 38px !important;
        padding: 0px !important;
        margin: 0px !important;
        box-shadow: none !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        text-align: center !important;
        transform: none !important;
    }}
    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stTextInput"]) button[kind="secondary"]:hover {{
        background: #F1F5F9 !important;
        color: #1A202C !important;
        border-color: rgba(49, 51, 63, 0.35) !important;
        box-shadow: none !important;
        transform: none !important;
    }}

    .dashboard-wrapper {{
        position: relative;
        display: inline-block;
        width: 100%;
        border-radius: 12px;
        overflow: hidden;
        background: transparent;
    }}
    .dashboard-wrapper img {{
        width: 100%;
        display: block;
        border-radius: 12px;
    }}
    .hover-download-btn {{
        position: absolute;
        top: 12px;
        right: 12px;
        background: rgba(30, 30, 30, 0.7);
        color: white !important;
        padding: 8px;
        border-radius: 8px;
        opacity: 0;
        transition: opacity 0.3s ease, background 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        text-decoration: none;
        backdrop-filter: blur(4px);
    }}
    .dashboard-wrapper:hover .hover-download-btn {{
        opacity: 1;
    }}
    .hover-download-btn:hover {{
        background: rgba(0, 0, 0, 0.9);
        color: #FFBF00 !important;
    }}

    [data-testid="stAlert"] {{
        background: linear-gradient(135deg, #FFBF00, #D9463E) !important;
        border: none !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3) !important;
    }}
    [data-testid="stAlert"] p, [data-testid="stAlert"] li, [data-testid="stAlert"] span {{
        color: #1A1D20 !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
    }}
    [data-testid="stAlert"] strong {{
        color: #000000 !important;
        font-weight: 900 !important;
    }}
    .gradient-box {{
        background: linear-gradient(135deg, #FFBF00, #D9463E) !important;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        overflow-x: auto;
        margin-bottom: 15px;
    }}
    .custom-dataframe {{
        width: 100%;
        border-collapse: collapse;
        color: #1A1D20 !important;
        font-weight: 600;
        font-size: 1.05rem;
    }}
    .custom-dataframe th {{
        background-color: {table_th_bg};
        color: {table_th_text};
        padding: 12px;
        text-align: left;
        border-bottom: 2px solid rgba(0,0,0,0.2);
        font-weight: 900;
    }}
    .custom-dataframe td {{
        padding: 10px 12px;
        border-bottom: 1px solid {table_td_border};
    }}
    </style>
""",
    unsafe_allow_html=True,
)

# 5. Headers
st.markdown('<h1 class="center-title">✨ AURA BI ✨</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="center-subtitle">The Autonomous Data Analyst</p>', unsafe_allow_html=True
)
st.markdown("---")

# 6. Suggestions
st.markdown("### 💡 Quick Try:")
col_sug1, col_sug2, col_sug3 = st.columns(3)

quick_query = None

with col_sug1:
    if st.button(
        "📦 Show total quantity ordered for each product category.",
        use_container_width=True,
    ):
        quick_query = "Show total quantity ordered for each product category."
with col_sug2:
    if st.button(
        "🌍 Which region generated the highest number of orders?",
        use_container_width=True,
    ):
        quick_query = "Which region generated the highest number of orders?"
with col_sug3:
    if st.button(
        "💰 What is the total revenue generated by each product category?",
        use_container_width=True,
    ):
        quick_query = "What is the total revenue generated by each product category?"

st.markdown("<br>", unsafe_allow_html=True)

# 7. Smart Integrated Input Section
st.markdown("### 🎙️ Ask your business question:")

if "query_input" not in st.session_state:
    st.session_state.query_input = ""


def clear_query():
    st.session_state.query_input = ""


col_input, col_clear, col_mic = st.columns([17, 1, 1], vertical_alignment="center")

with col_mic:
    spoken_text = speech_to_text(
        language="en",
        start_prompt="🎙️",
        stop_prompt="🛑",
        use_container_width=True,
        just_once=True,
        key="STT",
    )

if spoken_text:
    st.session_state.query_input = spoken_text

with col_clear:
    st.button("✕", key="clear_btn", on_click=clear_query, help="Clear input")

with col_input:
    user_question = st.text_input(
        "🔍 Search:",
        key="query_input",
        placeholder="Ask Aura BI or click the mic icon...",
        label_visibility="collapsed",
    )

# 8. LangGraph Execution & Session State Storage
st.markdown("<br>", unsafe_allow_html=True)
analyze_clicked = st.button("🚀 Analyze Data", type="primary")

active_question = quick_query if quick_query else user_question
should_run = quick_query is not None or (analyze_clicked and user_question)

# Initialize a session state variable to store our analysis results
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

# Only run the AI if the user actively asked a question
if should_run:
    with st.spinner("🤖 Aura is crunching the numbers... Please wait..."):
        if os.path.exists("latest_chart.png"):
            os.remove("latest_chart.png")

        initial_state = {
            "question": active_question,
            "sql_query": None,
            "is_safe": True,
            "data": None,
            "insights": None,
            "error": None,
            "retry_count": 0,
        }

        # Save the agent's output into session state so it survives button clicks!
        st.session_state.analysis_result = app_graph.invoke(initial_state)

# Unconditionally render the UI if we have a saved result in session state
if st.session_state.analysis_result:
    final_state = st.session_state.analysis_result

    if not final_state["is_safe"]:
        st.error(f"❌ Security Alert: {final_state['error']}")

    elif final_state["error"]:
        st.error(f"⚠️ SQL Execution Failed: {final_state['error']}")

    else:
        df = final_state["data"]
        st.success(
            f"✨ Analysis Complete! (Self-corrected in {final_state['retry_count']} retries)"
        )

        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown(
                f"<h3 style='color: {main_text};'>📋 Query Results</h3>",
                unsafe_allow_html=True,
            )
            if df is not None and not df.empty:
                table_html = df.to_html(index=False, classes="custom-dataframe")
                st.markdown(
                    f'<div class="gradient-box">{table_html}</div>',
                    unsafe_allow_html=True,
                )

                # 3 EQUAL EXPORT BUTTONS ROW
                btn_col1, btn_col2, btn_col3 = st.columns(3)

                with btn_col1:
                    pdf_data = generate_pdf(df)
                    st.download_button(
                        "📄 Export as PDF",
                        data=pdf_data,
                        file_name="aura_query_result.pdf",
                        mime="application/pdf",
                        type="primary",
                        use_container_width=True,
                    )

                with btn_col2:
                    buffer = io.BytesIO()
                    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                        df.to_excel(writer, index=False, sheet_name="Aura_Insights")
                    excel_data = buffer.getvalue()
                    st.download_button(
                        "📊 Export as Excel",
                        data=excel_data,
                        file_name="aura_query_result.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        type="primary",
                        use_container_width=True,
                    )

                with btn_col3:
                    csv = df.to_csv(index=False).encode("utf-8")
                    st.download_button(
                        "📥 Export as CSV",
                        data=csv,
                        file_name="aura_query_result.csv",
                        mime="text/csv",
                        type="primary",
                        use_container_width=True,
                    )

            else:
                st.warning(
                    "The query executed successfully, but returned 0 rows of data."
                )

        with col2:
            st.markdown(
                f"<h3 style='color: {main_text};'>📈 Visual Dashboard</h3>",
                unsafe_allow_html=True,
            )
            if os.path.exists("latest_chart.png"):
                chart_b64 = get_base64_image("latest_chart.png")
                chart_html = f"""
                <div class="dashboard-wrapper">
                    <img src="data:image/png;base64,{chart_b64}" alt="Dashboard Chart" />
                    <a href="data:image/png;base64,{chart_b64}" download="aura_dashboard_chart.png" class="hover-download-btn" title="Download Chart">
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                            <polyline points="7 10 12 15 17 10"></polyline>
                            <line x1="12" y1="15" x2="12" y2="3"></line>
                        </svg>
                    </a>
                </div>
                """
                st.markdown(chart_html, unsafe_allow_html=True)
            else:
                st.info(
                    "ℹ️ No visual chart generated. Auto-charting requires exactly 2 columns of data."
                )

        st.markdown("---")
        st.markdown(
            f"<h2 style='text-align: center; color: #FFBF00;'>💡 Executive Business Insights</h2>",
            unsafe_allow_html=True,
        )

        if final_state.get("insights"):
            st.info(final_state["insights"])
        else:
            st.warning("Insights could not be generated by the AI.")

st.markdown("---")
st.markdown(
    f"<p style='text-align: center; color: {sub_text}; font-weight: 500;'>Aura BI | Engineered with Python, LangGraph, MySQL & Groq & by AJ :)</p>",
    unsafe_allow_html=True,
)