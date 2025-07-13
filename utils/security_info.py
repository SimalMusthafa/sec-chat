import streamlit as st

def render_how_it_works():
    st.markdown("""
    <div style="background:#1b2230;border-radius:14px;padding:25px 32px 20px 32px; color:#e7ebf7">
    <h3>🔐 How SecureKey Messenger Works</h3>
    <ul>
      <li>We use modern <b>public-key cryptography</b> based on the <b>Curve25519 (X25519)</b> algorithm.</li>
      <li><b>Your private key</b> never leaves your device. You generate or import it, and keep it secret.</li>
      <li>To send a message, you use the recipient's <b>public key</b> to encrypt the message securely.</li>
      <li>The encrypted message can only be decrypted by the owner of the matching private key.</li>
      <li>Messages are encrypted and decrypted <b>locally</b> in your browser, so no plaintext is ever sent or stored on the server.</li>
      <li>You can download and share key files and encrypted messages safely as JSON files.</li>
      <li>The app also generates QR codes for easy sharing of public keys.</li>
    </ul>
    <hr>
    <b>Security Tips:</b> Never share your private key. Only share your public key or its QR code.
    </div>
    """, unsafe_allow_html=True)

def render_faq():
    st.markdown("""
    <div style="background:#22263b;border-radius:14px;padding:25px 32px 20px 32px; color:#c7d0e5">
    <h3>❓ Frequently Asked Questions</h3>
    <b>Q: What is public-key cryptography?</b><br>
    <i>A:</i> It is a system where you have a pair of keys: a public key to encrypt messages, and a private key to decrypt them.<br><br>
    <b>Q: Can anyone read my messages?</b><br>
    <i>A:</i> No, only the holder of the private key corresponding to the public key used can decrypt the message.<br><br>
    <b>Q: How do I keep my private key safe?</b><br>
    <i>A:</i> Store your private key JSON file securely and never share it. Losing it means you cannot decrypt messages.<br><br>
    <b>Q: What if I lose my key?</b><br>
    <i>A:</i> You will not be able to decrypt messages sent to you. Always back up your private key safely.<br><br>
    <b>Q: Is this like Signal or WhatsApp?</b><br>
    <i>A:</i> No, this app is designed for one-off encrypted message exchange, not instant messaging.<br><br>
    <b>Q: Can I use this for group messages?</b><br>
    <i>A:</i> Not currently. Each message is encrypted for one recipient’s public key.<br><br>
    <b>Q: Can I trust this app with my private key?</b><br>
    <i>A:</i> The app does not send your private key anywhere. Encryption and decryption happen locally in your browser.<br><br>
    <b>Q: How do I share my public key?</b><br>
    <i>A:</i> Share the public key string or the QR code generated in the app.<br><br>
    </div>
    """, unsafe_allow_html=True)
