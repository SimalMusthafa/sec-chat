import streamlit as st
from utils.crypto_utils import (
    generate_keypair, save_keypair_json, load_keypair_json,
    encrypt_with_public_key, decrypt_with_private_key,
    public_key_to_qr
)
from utils.ui_helpers import main_css, show_banner, copy_button, beautiful_card
from utils.security_info import render_how_it_works, render_faq

st.set_page_config(page_title="🔑 SecureKey Exchange Messenger", layout="centered")
main_css()
st.title("🔑 SecureKey Messenger: Public Key Encryption for Private Messaging")

tab1, tab2, tab3 = st.tabs([
    "1️⃣ Generate/Import Keypair",
    "2️⃣ Encrypt & Send Message",
    "3️⃣ Decrypt Received Message"
])

# ---- Generate Keypair ----
with tab1:
    st.header("Generate or Import Your Keypair")
    beautiful_card("""
        <b>Generate a new secure keypair</b> for yourself, or <b>import your existing private key</b>.<br>
        <ul>
        <li><b>Keep your Private Key file secret!</b></li>
        <li>Share only your Public Key (or QR) with others.</li>
        </ul>
    """)
    key_method = st.radio("Keypair setup:", ["Generate random keypair", "Import private key (JSON file)", "Create from passphrase"])
    if key_method == "Generate random keypair":
        if st.button("Generate Keypair"):
            pub, priv = generate_keypair()
            st.success("Keypair generated!")
            key_json = save_keypair_json(pub, priv)
            st.markdown("#### Download Your Keypair (Private!):")
            st.download_button("Download Private Key JSON", data=key_json, file_name="private_key.json", mime="application/json")
            st.markdown("#### Your Public Key (safe to share):")
            st.code(pub, language="text")
            copy_button(pub, "Copy Public Key")
            st.markdown("Or scan QR code to share public key securely:")
            st.image(public_key_to_qr(pub))
    elif key_method == "Import private key (JSON file)":
        up = st.file_uploader("Upload your private key JSON file", type="json")
        if up:
            try:
                pub, priv = load_keypair_json(up.read())
                st.success("Keypair loaded!")
                st.code(pub, language="text")
                st.markdown("Ready to decrypt messages sent to your public key.")
            except Exception:
                show_banner("Invalid or corrupted private key file.", "error")
    elif key_method == "Create from passphrase":
        passphrase = st.text_input("Enter passphrase (min 12 chars)", type="password")
        if st.button("Create Keypair from Passphrase"):
            if not passphrase or len(passphrase) < 12:
                show_banner("Passphrase must be at least 12 characters.", "error")
            else:
                pub, priv = generate_keypair(passphrase=passphrase)
                st.success("Deterministic keypair created from passphrase.")
                key_json = save_keypair_json(pub, priv)
                st.download_button("Download Private Key JSON", data=key_json, file_name="private_key.json", mime="application/json")
                st.code(pub, language="text")
                copy_button(pub, "Copy Public Key")
                st.image(public_key_to_qr(pub))

# ---- Encrypt Message ----
with tab2:
    st.header("Encrypt a Message for Someone")
    beautiful_card("""
        <b>Paste the recipient's public key</b> (from QR or text), write your message, and get an encrypted file to send them.<br>
        <ul><li><b>Your message is encrypted with their public key.</b> Only they can decrypt with their private key.</li></ul>
    """)
    pubkey = st.text_area("Recipient's Public Key", height=80)
    msg = st.text_area("Your message", height=150, max_chars=4000)
    if st.button("Encrypt & Download"):
        if not pubkey.strip():
            show_banner("Paste the recipient's public key.", "error")
        elif not msg.strip():
            show_banner("Enter your message to encrypt.", "error")
        else:
            try:
                encrypted_json = encrypt_with_public_key(pubkey, msg)
                st.success("Message encrypted! Download below.")
                st.download_button(
                    "Download Encrypted Message JSON",
                    data=encrypted_json,
                    file_name="encrypted_message.json",
                    mime="application/json"
                )
                st.code(encrypted_json[:400] + "...", language="json")
            except Exception as e:
                show_banner(f"Encryption failed: {e}", "error")

# ---- Decrypt Message ----
with tab3:
    st.header("Decrypt a Received Message")
    beautiful_card("""
        <b>Load your private key file and the encrypted message file you received.</b><br>
        <ul>
        <li>Private key file: <b>private_key.json</b></li>
        <li>Encrypted message file: <b>encrypted_message.json</b></li>
        </ul>
    """)
    privkey_file = st.file_uploader("Upload your private key JSON", type="json", key="privkeyu")
    enc_file = st.file_uploader("Upload encrypted message JSON", type="json", key="encfileu")
    if st.button("Decrypt Message"):
        if not privkey_file or not enc_file:
            show_banner("Upload both your private key and the encrypted message.", "error")
        else:
            try:
                pub, priv = load_keypair_json(privkey_file.read())
                plaintext = decrypt_with_private_key(priv, enc_file.read())
                beautiful_card(f"<b>Decrypted Message:</b><br><br>{plaintext}")
                st.balloons()
            except Exception as e:
                show_banner(f"Decryption failed: {e}", "error")

st.markdown("---")
with st.expander("🔍 See how it works / FAQ"):
    render_how_it_works()
    render_faq()
