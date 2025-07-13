import streamlit as st
import time
from utils.crypto_utils import generate_key, encrypt_message, decrypt_message, derive_key_from_passphrase
from utils.storage import store_message, retrieve_message, delete_message, purge_expired
from utils.ui_helpers import main_css, message_card, show_banner, copy_button
from utils.security_info import render_how_it_works, render_faq

st.set_page_config(page_title="🔐 SecureMsg - End-to-End Encrypted Messenger", layout="centered")

main_css()  # Inject custom CSS

st.title("🔐 SecureMsg: End-to-End Encrypted Message Exchange")

# ---- Purge expired messages on each run ----
purge_expired()

# ---- Page navigation ----
page = st.sidebar.radio(
    "Menu", 
    ["📤 Send Secure Message", "📥 Retrieve Message", "ℹ️ How This Works", "❓ FAQ"]
)

# ---- Send Secure Message ----
if page == "📤 Send Secure Message":
    st.header("Send a Secure Message")
    with st.form("send_form"):
        msg = st.text_area("Your message", height=140, max_chars=3000)
        option = st.radio("Choose encryption method:", ["Generate random code", "Use my own passphrase"])
        if option == "Generate random code":
            key = generate_key()
            key_display = key.hex()
            passphrase = None
        else:
            passphrase = st.text_input("Passphrase (min 10 chars)", type="password", max_chars=100)
            key_display = None
            key = None
        expiry = st.selectbox("Message expires after:", ["15 minutes", "1 hour", "12 hours", "1 day"], index=1)
        submitted = st.form_submit_button("Encrypt & Generate Link")
    
    if submitted:
        if not msg.strip():
            show_banner("Please enter a message.", "error")
        elif option == "Use my own passphrase" and (not passphrase or len(passphrase) < 10):
            show_banner("Passphrase must be at least 10 characters.", "error")
        else:
            # Key derivation
            if option == "Use my own passphrase":
                key = derive_key_from_passphrase(passphrase)
            # Encrypt
            nonce, ct, tag = encrypt_message(msg, key)
            # Store encrypted
            expire_at = time.time() + {"15 minutes":900, "1 hour":3600, "12 hours":43200, "1 day":86400}[expiry]
            msg_id = store_message(nonce, ct, tag, expire_at)
            # Show result
            st.success("Your encrypted message is ready!")
            link = f"{st.secrets.get('PUBLIC_URL', 'https://securemsg.yourdomain.com')}/?msgid={msg_id}"
            st.markdown(f"**Share this code (or link) with the recipient:**")
            if option == "Generate random code":
                st.text_area("Decryption Code", value=key_display, height=36, key="key_display", help="Copy and send to your recipient.", disabled=True)
                copy_button(key_display, "Copy Code")
            else:
                st.text_area("Passphrase", value=passphrase, height=36, key="passphrase_display", help="Copy and send to your recipient.", disabled=True)
                copy_button(passphrase, "Copy Passphrase")
            st.markdown(f"**Message Link:**")
            st.code(link, language="text")
            copy_button(link, "Copy Link")
            st.info("This message can be read only ONCE. It will self-destruct after reading, or after expiry (whichever comes first).")

# ---- Retrieve Secure Message ----
elif page == "📥 Retrieve Message":
    st.header("Retrieve & Decrypt Message")
    with st.form("retrieve_form"):
        msg_id = st.text_input("Message Code or Link")
        method = st.radio("Enter code or passphrase?", ["Random code", "Passphrase"])
        code = st.text_input("Enter decryption code or passphrase", type="password")
        submitted = st.form_submit_button("Decrypt Message")
    if submitted:
        if not msg_id.strip():
            show_banner("Please paste your code or link.", "error")
        elif not code or len(code) < 10:
            show_banner("Please enter a valid code/passphrase.", "error")
        else:
            # Parse msgid from link or code
            _id = msg_id
            if "?msgid=" in msg_id:
                _id = msg_id.split("?msgid=")[-1]
            enc_data = retrieve_message(_id)
            if not enc_data:
                show_banner("Message not found or has expired/self-destructed.", "error")
            else:
                nonce, ct, tag, expire_at = enc_data
                try:
                    if method == "Random code":
                        key = bytes.fromhex(code)
                    else:
                        key = derive_key_from_passphrase(code)
                    plaintext = decrypt_message(nonce, ct, tag, key)
                    # Delete after read (self-destruct)
                    delete_message(_id)
                    message_card(plaintext)
                    st.balloons()
                except Exception:
                    show_banner("Failed to decrypt. Wrong code or message corrupted.", "error")
                st.info("This message is now deleted and cannot be read again.")

# ---- How it Works ----
elif page == "ℹ️ How This Works":
    render_how_it_works()

# ---- FAQ ----
elif page == "❓ FAQ":
    render_faq()
