"""
Configuration settings for the Color Palette Generator application.
"""

# Application Settings
APP_NAME = "Color Palette Generator"
DEBUG_MODE = True
SECRET_KEY = "your-secret-key-here"  # Change in production

# Feature Flags
ENABLE_KEYWORD_SUGGESTIONS = True
ENABLE_COPY_TO_CLIPBOARD = True
ENABLE_TOAST_NOTIFICATIONS = True
ENABLE_MOBILE_OPTIMIZATION = True
ENABLE_DYNAMIC_BACKGROUNDS = True

# Color Generation Settings
DEFAULT_PALETTE_SIZE = 5
MIN_BRIGHTNESS = 0.3
MAX_BRIGHTNESS = 1.0
MIN_SATURATION = 0.2
MAX_SATURATION = 1.0

# UI Settings
MAX_DESCRIPTION_LENGTH = 100
TOAST_DURATION_MS = 3000
MOBILE_BREAKPOINT_PX = 768

# Cache Settings
ENABLE_CACHE = True
CACHE_TIMEOUT = 300  # 5 minutes

# API Rate Limiting
RATE_LIMIT_ENABLED = True
RATE_LIMIT_PER_MINUTE = 60
