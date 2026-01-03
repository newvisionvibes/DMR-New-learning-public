# File: modules/__init__.py
# ✅ FIXED VERSION - RESOLVES CIRCULAR IMPORT
# Status: Production Ready
# Date: 2026-01-01

"""
Module initialization - SAFE LAZY IMPORTS (no circular dependencies)
Only import utilities here, NOT app renderers
"""

# ✅ Safe to import: Utilities and configurations
__version__ = "1.0.0"
__author__ = "ETF RS Analysis Team"

# Optional: Import only if needed elsewhere
# Avoid importing tab_renderers here to prevent circular imports
