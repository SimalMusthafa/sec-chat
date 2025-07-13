import streamlit as st

def render_how_it_works():
    st.markdown("""
    <div style="background:#1b2230;border-radius:14px;padding:25px 32px 20px 32px; color:#e7ebf7">
    <h3>🔐 How SecureMsg Works</h3>
    <ul>
      <li>All messages are <b>encrypted</b> <span style="color:#4dd0e1">on your device</span> with <b>AES-256-GCM</b> before being stored or transmitted.</li>
      <li>You choose either a strong passphrase <i>or</i> a randomly generated secure code as the key.</li>
      <li>We <b>never</b> store your passphrase, key, or decrypted message—only the encrypted blob.</li>
      <li>When the message is read, it is <b>immediately deleted</b> (self-destructs). You can also set a time-to-expiry.</li>
      <li>Even if the database/server is breached, <b>your messages cannot be decrypted</b> without the key.</li>
      <li><b>Encryption details:</b>
        <ul>
            <li>Symmetric: <b>AES-256-GCM</b> with fresh random key or scrypt-derived key per message.</li>
            <li>Strong key derivation: <b>scrypt</b> (modern, slow, brute-force resistant) for passphrases.</li>
            <li>Authenticated encryption: ensures your message <b>cannot be tampered with</b>.</li>
        </ul>
      </li>
    </ul>
    <hr>
    <b>Pro Tip:</b> Never share your code/passphrase over insecure channels. For best security, use a randomly generated code.
    </div>
    """, unsafe_allow_html=True)

def render_faq():
    st.markdown("""
    <div style="background:#22263b;border-radius:14px;padding:25px 32px 20px 32px; color:#c7d0e5">
    <h3>❓ Frequently Asked Questions</h3>
    <b>Q: Is this like Signal/WhatsApp?</b><br>
    <i>A:</i> No, SecureMsg is for sending one-off, highly secure messages. It does not do live chat or instant notifications.<br><br>
    <b>Q: Can you or the server read my messages?</b><br>
    <i>A:</i> No. All encryption/decryption happens with your key/passphrase. The server only stores encrypted blobs.<br><br>
    <b>Q: What happens if I lose my code or passphrase?</b><br>
    <i>A:</i> You cannot decrypt the message. There is no backdoor or recovery—this is by design.<br><br>
    <b>Q: How long is my message kept?</b><br>
    <i>A:</i> Until it is read (then deleted instantly) or the expiry time is reached.<br><br>
    <b>Q: What if two people try to open the same message?</b><br>
    <i>A:</i> Only the first to decrypt will succeed; the message will self-destruct after being opened once.<br><br>
    <b>Q: Can I send files?</b><br>
    <i>A:</i> Not yet, but you can paste base64-encoded data or secret text.<br><br>
    <b>Q: Is it safe to use a passphrase?</b><br>
    <i>A:</i> Yes, but use a strong, unique passphrase (at least 10-12 random characters). For maximum security, use a generated code.<br><br>
    <b>Q: Is this open source?</b><br>
    <i>A:</i> Yes, so you (or your company) can audit and run it yourself!
    </div>
    """, unsafe_allow_html=True)
