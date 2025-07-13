import streamlit as st
import time

from utils.crypto_utils import (
    generate_keypair,
    save_keypair_json,
    load_keypair_json,
    encrypt_with_public_key,
    decrypt_with_private_key,
    public_key_to_qr,
)
from utils.storage import purge_expired
from utils.ui_helpers import main_css, beautiful_card, show_banner, copy_button
from utils.security_info import render_how_it_works, render_faq

st.set_page_config(page_title="🔑 SecureKey Exchange Messenger", layout="centered")
main_css()
st.title("🔑 SecureKey Messenger: Public-Key Encrypted Messaging")

# Purge any expired stored messages (if using storage)
purge_expired()

# Ensure session state for keys and encrypted payload
if 'pub_key' not in st.session_state:
    st.session_state.pub_key = None
if 'priv_key' not in st.session_state:
    st.session_state.priv_key = None
if 'encrypted_json' not in st.session_state:
    st.session_state.encrypted_json = None

tab1, tab2, tab3 = st.tabs([
    "1️⃣ Generate/Import Keypair",
    "2️⃣ Encrypt & Send Message",
    "3️⃣ Decrypt Received Message"
])

# === Tab 1: Keypair Generation/Import ===
with tab1:
    st.header("🔑 Keypair Setup")
    beautiful_card("""
        Generate a new keypair or import your existing private key.
        Keep your <b>private key</b> secret; share only your <b>public key</b>.
    """)
    method = st.radio("Keypair action:", [
        "Generate random keypair",
        "Import private key (JSON)",
        "Create deterministic from passphrase"
    ])

    if method == "Generate random keypair":
        if st.button("Generate Keypair"):
            pub, priv = generate_keypair()
            st.session_state.pub_key = pub
            st.session_state.priv_key = priv
            st.success("🔑 Keypair generated!")

    elif method == "Import private key (JSON)":
        uploaded = st.file_uploader("Upload your private_key.json", type="json")
        if uploaded:
            try:
                pub, priv = load_keypair_json(uploaded.read())
                st.session_state.pub_key = pub
                st.session_state.priv_key = priv
                st.success("🔑 Keypair imported!")
            except Exception:
                show_banner("Invalid private key file.", "error")

    else:  # passphrase
        passphrase = st.text_input("Enter passphrase (min 12 chars)", type="password")
        if st.button("Derive Keypair from Passphrase"):
            if not passphrase or len(passphrase) < 12:
                show_banner("Passphrase must be ≥12 characters.", "error")
            else:
                pub, priv = generate_keypair(passphrase=passphrase)
                st.session_state.pub_key = pub
                st.session_state.priv_key = priv
                st.success("🔑 Deterministic keypair created!")

    # Display and download once keys are in state
    if st.session_state.priv_key:
        key_json = save_keypair_json(
            st.session_state.pub_key,
            st.session_state.priv_key
        )
        st.markdown("**Your Private Key (keep it secret):**")
        st.download_button(
            "⬇️ Download private_key.json",
            data=key_json,
            file_name="private_key.json",
            mime="application/json"
        )
        st.markdown("**Your Public Key (safe to share):**")
        st.code(st.session_state.pub_key, language="text")
        copy_button(st.session_state.pub_key, "Copy Public Key")
        st.markdown("**Or share via QR code:**")
        st.image(public_key_to_qr(st.session_state.pub_key))

# === Tab 2: Encrypt & Send Message ===
with tab2:
    st.header("✉️ Encrypt & Send Message")
    beautiful_card("""
        Paste your recipient’s public key, type your message, and download the encrypted JSON file to send them.
    """)
    # Encryption form
    with st.form("encrypt_form"):
        pubkey = st.text_area(
            "Recipient's Public Key",
            height=80,
            key="encrypt_pubkey"
        )
        message = st.text_area(
            "Message to encrypt",
            height=150,
            max_chars=4000,
            key="encrypt_message"
        )
        submit_encrypt = st.form_submit_button("🔒 Encrypt Message")

    if submit_encrypt:
        if not pubkey.strip():
            show_banner("Enter the recipient’s public key.", "error")
        elif not message.strip():
            show_banner("Enter a message to encrypt.", "error")
        else:
            try:
                st.session_state.encrypted_json = encrypt_with_public_key(
                    pubkey, message
                )
                st.success("🔒 Message encrypted! Ready to download below.")
            except Exception as e:
                show_banner(f"Encryption error: {e}", "error")

    # Download and preview (outside the form)
    if st.session_state.encrypted_json:
        st.download_button(
            "⬇️ Download encrypted_message.json",
            data=st.session_state.encrypted_json,
            file_name="encrypted_message.json",
            mime="application/json"
        )
        preview = st.session_state.encrypted_json
        st.code(
            preview if len(preview) < 500 else preview[:500] + "...",
            language="json"
        )

# === Tab 3: Decrypt Received Message ===
with tab3:
    st.header("🔓 Decrypt Received Message")
    beautiful_card("""
        Upload your private key JSON and the encrypted message JSON to decrypt.
    """)
    priv_file = st.file_uploader(
        "Upload your private_key.json",
        type="json",
        key="privkey"
    )
    enc_file = st.file_uploader(
        "Upload encrypted_message.json",
        type="json",
        key="encfile"
    )
    if st.button("Decrypt Message"):
        if not priv_file or not enc_file:
            show_banner("Both files are required.", "error")
        else:
            try:
                pub, priv = load_keypair_json(priv_file.read())
                plaintext = decrypt_with_private_key(
                    priv, enc_file.read()
                )
                beautiful_card(f"<b>Decrypted Message:</b><br><br>{plaintext}")
                st.balloons()
            except Exception as e:
                show_banner(f"Decryption error: {e}", "error")

# === Footer: How It Works & FAQ ===
st.markdown("---")
with st.expander("🔍 How it works & FAQ"):
    render_how_it_works()
    render_faq()
