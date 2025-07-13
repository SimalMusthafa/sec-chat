import json
import base64
from nacl.public import PrivateKey, PublicKey, SealedBox
from nacl.encoding import Base64Encoder
import qrcode
from io import BytesIO
import hashlib

def generate_keypair(passphrase=None):
    """
    Generates a X25519 keypair.
    If passphrase is provided, derives deterministic keypair from passphrase using SHA256.
    Returns (public_key_b64, private_key_b64)
    """
    if passphrase:
        h = hashlib.sha256(passphrase.encode("utf-8")).digest()
        priv = PrivateKey(h)
    else:
        priv = PrivateKey.generate()
    pub = priv.public_key
    return (
        base64.b64encode(pub.encode()).decode(),
        base64.b64encode(priv.encode()).decode()
    )

def save_keypair_json(pub_b64, priv_b64):
    obj = {
        "public_key": pub_b64,
        "private_key": priv_b64
    }
    return json.dumps(obj, indent=2)

def load_keypair_json(file_bytes):
    obj = json.loads(file_bytes.decode() if isinstance(file_bytes, bytes) else file_bytes)
    pub_b64 = obj["public_key"]
    priv_b64 = obj["private_key"]
    return pub_b64, priv_b64

def encrypt_with_public_key(recipient_pub_b64, message: str):
    """
    Encrypts the message with recipient's public key using X25519 + SealedBox.
    Returns a JSON string containing the encrypted message.
    """
    pub = PublicKey(base64.b64decode(recipient_pub_b64))
    box = SealedBox(pub)
    ct = box.encrypt(message.encode("utf-8"), encoder=Base64Encoder)
    obj = {
        "version": 1,
        "encrypted_message": ct.decode()
    }
    return json.dumps(obj, indent=2)

def decrypt_with_private_key(priv_b64, encrypted_json_bytes):
    """
    Decrypts a message using the provided private key (base64), and encrypted message JSON (bytes or str).
    Returns the decrypted plaintext (str).
    """
    priv = PrivateKey(base64.b64decode(priv_b64))
    box = SealedBox(priv)
    enc_obj = json.loads(encrypted_json_bytes.decode() if isinstance(encrypted_json_bytes, bytes) else encrypted_json_bytes)
    ct = base64.b64decode(enc_obj["encrypted_message"])
    pt = box.decrypt(ct).decode("utf-8")
    return pt

def public_key_to_qr(pub_b64):
    """
    Returns a QR code PNG image (as BytesIO) of the public key (base64).
    """
    img = qrcode.make(pub_b64)
    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf
