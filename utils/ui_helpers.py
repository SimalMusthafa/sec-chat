import streamlit as st

def main_css():
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(120deg, #232946 0%, #161925 100%);
        font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif;
    }
    h1, h2, h3, h4, h5 { color: #f7fafc !important; }
    .block-container { padding-top: 2.5rem; }
    .beautiful-card {
        background: #253056;
        border-radius: 18px;
        padding: 22px 28px 16px 28px;
        margin: 22px auto 18px auto;
        color: #f7fafc;
        box-shadow: 0 6px 30px #0003;
        font-size: 1.14em;
        word-break: break-word;
    }
    .copy-btn {
        margin-left: 12px;
        padding: 6px 16px;
        background: #384975;
        color: #fff;
        border: none;
        border-radius: 9px;
        cursor: pointer;
        font-size: 0.98em;
    }
    .custom-banner {
        border-radius: 12px;
        padding: 12px 18px;
        margin-bottom: 18px;
        font-size: 1.04em;
        background: #1b202a;
        color: #f44336;
        border-left: 7px solid #e94560;
    }
    .custom-banner.success {
        background: #232f1b;
        color: #73c35e;
        border-left: 7px solid #73c35e;
    }
    .custom-banner.info {
        background: #1a2537;
        color: #36a2f4;
        border-left: 7px solid #36a2f4;
    }
    </style>
    """, unsafe_allow_html=True)

def show_banner(msg, type="error"):
    color = {
        "error": "custom-banner",
        "success": "custom-banner success",
        "info": "custom-banner info"
    }.get(type, "custom-banner")
    st.markdown(f"<div class='{color}'>{msg}</div>", unsafe_allow_html=True)

def beautiful_card(html):
    st.markdown(f"<div class='beautiful-card'>{html}</div>", unsafe_allow_html=True)

def copy_button(text, label="Copy"):
    import uuid
    key = str(uuid.uuid4()).replace('-', '')[:10]
    btn = st.button(f"{label}", key=f"copy_{key}")
    if btn:
        js = f"""
        <script>
        navigator.clipboard.writeText("{text.replace('"', '\\"')}");
        </script>
        """
        st.markdown(js, unsafe_allow_html=True)
        st.success("Copied!")
