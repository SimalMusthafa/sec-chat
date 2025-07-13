import os
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# -- Constants --
KEYLEN = 32  # 256-bit AES
NONCE_SIZE = 12  # Recommended for AES-GCM

def generate_key():
    """
    Generate a random 256-bit key for AES-GCM.
    Returns bytes.
    """
    return os.urandom(KEYLEN)

def derive_key_from_passphrase(passphrase: str, salt: bytes = None):
    """
    Derive a 256-bit key from passphrase using scrypt KDF (secure, slow, modern).
    Uses random salt (per message), or a fixed one for demo if needed.
    Returns key (bytes). For real systems, save the salt alongside the message!
    """
    if salt is None:
        salt = b"SecureMsgSalt"  # For demo; in production use random salt per message!
    kdf = Scrypt(
        salt=salt,
        length=KEYLEN,
        n=2**15,
        r=8,
        p=1,
    )
    key = kdf.derive(passphrase.encode("utf-8"))
    return key

def encrypt_message(plaintext: str, key: bytes):
    """
    Encrypt plaintext string using AES-GCM.
    Returns (nonce, ciphertext, tag), all as bytes.
    """
    aesgcm = AESGCM(key)
    nonce = os.urandom(NONCE_SIZE)
    ct = aesgcm.encrypt(nonce, plaintext.encode("utf-8"), None)
    # GCM tag is last 16 bytes of ct
    tag = ct[-16:]
    return nonce, ct, tag

def decrypt_message(nonce: bytes, ciphertext: bytes, tag: bytes, key: bytes):
    """
    Decrypt using AES-GCM.
    Returns plaintext string.
    """
    aesgcm = AESGCM(key)
    # Combine ct+tag if needed (ct always contains tag in AESGCM lib)
    pt = aesgcm.decrypt(nonce, ciphertext, None)
    return pt.decode("utf-8")
