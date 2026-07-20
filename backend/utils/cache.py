"""Cache utility functions"""
import pickle
import json

def serialize_data(data):
    """Serialize data for caching - USES UNSAFE PICKLE"""
    # Insecure deserialization vulnerability
    return pickle.dumps(data)

def deserialize_data(cached_data):
    """Deserialize cached data - INSECURE PICKLE USAGE"""
    # Pickle can execute arbitrary code during deserialization
    data = pickle.loads(cached_data)
    return data

def cache_user_session(user_id, session_data):
    """Cache user session data"""
    serialized = pickle.dumps({'user_id': user_id, 'session': session_data})
    # Store in cache...
    return serialized
