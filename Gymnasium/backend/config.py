import yaml
from datetime import timedelta

# Load config from yaml
with open('config.yml', 'r') as f:
    config = yaml.safe_load(f)

# JWT settings
JWT_SECRET = config.get('JWT_SECRET', 'your-secret-key')
JWT_EXPIRATION_DAYS = config.get('JWT_EXPIRATION_DAYS', 1)
JWT_EXPIRATION = timedelta(days=JWT_EXPIRATION_DAYS) 