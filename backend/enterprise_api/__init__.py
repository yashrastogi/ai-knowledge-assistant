"""Enterprise API Integration Module

This module provides mock enterprise APIs for CMDB and ITSM services.
"""
from .cmdb_service import cmdb_service, CMDBService
from .itsm_service import itsm_service, ITSMService

__all__ = [
    'cmdb_service',
    'CMDBService',
    'itsm_service',
    'ITSMService',
]
