**SecureKey Messenger**

*End-to-End Public-Key Encrypted Messaging in Your Browser*

---

SecureKey Messenger lets you securely exchange one-off messages using modern public-key cryptography. All encryption and decryption happens in your browser—no plaintext ever leaves your device.

## 🚀 Features

1. **Generate or Import Keypair**

   * Create a brand-new X25519 keypair with one click.
   * Or import an existing private key (JSON) you’ve generated elsewhere.
   * Optionally derive a deterministic keypair from a passphrase.
   * Download your **private\_key.json** (keep this secret!) and share your public key or QR code.

2. **Encrypt & Send Message**

   * Paste your recipient’s public key into the form.
   * Type your confidential message.
   * Click “Encrypt Message” to produce a standalone **encrypted\_message.json** file.
   * No message plaintext is ever sent to the server—only the encrypted blob.

3. **Decrypt Received Message**

   * Upload your **private\_key.json** and the **encrypted\_message.json** you received.
   * Click “Decrypt Message” to reveal the original text.
   * Each message can only be decrypted once.

4. **Beautiful, Intuitive UI**

   * Step-by-step tabs guide you through key generation, encryption, and decryption.
   * Clear banners and cards surface success, errors, and instructions.
   * Copy-to-clipboard and QR code support for easy key sharing.

5. **Zero-Trust, Zero-Knowledge**

   * Private keys never leave your browser or server.
   * No plaintext storage anywhere—only encrypted JSON files.
   * Perfect for one-off secure notes, sensitive instructions, or private reminders.

## 📥 Getting Started

1. **Clone the repo**

   ```bash
   git clone https://github.com/youruser/securekey-messenger.git
   cd securekey-messenger
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**

   ```bash
   streamlit run app.py
   ```

4. **Open** [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🔒 How It Works

Under the hood, SecureKey Messenger uses X25519 (Curve25519) and NaCl’s SealedBox:

* **Keypair generation** creates a 32-byte private key and corresponding public key.
* **Encryption** with the recipient’s public key ensures only their private key can decrypt.
* **Decryption** uses your private key plus the ephemeral encryption metadata to recover the exact message.

All JSON files contain only Base64-encoded keys or ciphertext—no secrets are transmitted to the server.

---

## ❓ FAQ

**Q: What happens if I lose my private key?**
A: You won’t be able to decrypt any messages sent to that key. Always back it up securely!

**Q: Can I reuse the same keypair?**
A: Yes. You can generate once and import your private\_key.json any time.

**Q: Is my message safe if the server is breached?**
A: Absolutely. Only ciphertext is ever stored; without your private key, it’s unreadable.

**Q: Can I use passphrase-derived keys?**
A: Yes! For predictable, deterministic keypairs, you can derive directly from a strong passphrase.

---

## 📜 License

This project is open-source under the MIT License. See [LICENSE](LICENSE) for details.

---

Happy encrypting! 🛡️🔑
