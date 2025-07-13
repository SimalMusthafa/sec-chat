import time
import threading

# In-memory store (msgid: (nonce, ciphertext, tag, expire_at))
_MSG_STORE = {}

def store_message(nonce: bytes, ct: bytes, tag: bytes, expire_at: float) -> str:
    """
    Stores encrypted message and returns a message ID.
    The ID is a random hex token.
    """
    msg_id = _random_id()
    _MSG_STORE[msg_id] = (nonce, ct, tag, expire_at)
    return msg_id

def retrieve_message(msg_id: str):
    """
    Retrieve encrypted message by ID.
    Returns (nonce, ct, tag, expire_at) or None if not found or expired.
    """
    item = _MSG_STORE.get(msg_id)
    if not item:
        return None
    nonce, ct, tag, expire_at = item
    if time.time() > expire_at:
        # Expired, delete
        delete_message(msg_id)
        return None
    return nonce, ct, tag, expire_at

def delete_message(msg_id: str):
    """
    Remove a message after it is read.
    """
    if msg_id in _MSG_STORE:
        del _MSG_STORE[msg_id]

def purge_expired():
    """
    Periodically purge expired messages.
    (Runs each time the app reloads.)
    """
    now = time.time()
    to_del = [mid for mid, v in _MSG_STORE.items() if now > v[3]]
    for mid in to_del:
        del _MSG_STORE[mid]

def _random_id():
    """
    Generates a random message ID (10 bytes, hex).
    """
    import os
    return os.urandom(10).hex()
