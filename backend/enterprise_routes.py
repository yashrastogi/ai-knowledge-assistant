"""API routes for enterprise CMDB and ITSM queries"""
from fastapi import APIRouter, HTTPException, status
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enterprise_api import cmdb_service, itsm_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/enterprise", tags=["enterprise"])


# Request/Response Models
class CMDBSearchRequest(BaseModel):
    """Request model for CMDB search"""
    ci_type: Optional[str] = Field(None, description="CI type to filter by")
    status: Optional[str] = Field(None, description="Status to filter by")
    environment: Optional[str] = Field(None, description="Environment to filter by")
    owner: Optional[str] = Field(None, description="Owner team to filter by")
    name: Optional[str] = Field(None, description="Name to search for (partial match)")


class IncidentSearchRequest(BaseModel):
    """Request model for incident search"""
    priority: Optional[str] = Field(None, description="Priority to filter by")
    status: Optional[str] = Field(None, description="Status to filter by")
    affected_ci: Optional[str] = Field(None, description="Affected CI to filter by")
    assigned_to: Optional[str] = Field(None, description="Assigned team to filter by")
    category: Optional[str] = Field(None, description="Category to filter by")


class ChangeSearchRequest(BaseModel):
    """Request model for change search"""
    change_type: Optional[str] = Field(None, description="Type to filter by")
    status: Optional[str] = Field(None, description="Status to filter by")
    priority: Optional[str] = Field(None, description="Priority to filter by")
    affected_ci: Optional[str] = Field(None, description="Affected CI to filter by")


# CMDB Endpoints
@router.get("/cmdb/ci/{ci_id}")
async def get_configuration_item(ci_id: str):
    """Get a configuration item by ID
    
    Args:
        ci_id: Configuration item ID
        
    Returns:
        Configuration item details
    """
    logger.info(f"GET /cmdb/ci/{ci_id}")
    
    ci = cmdb_service.get_ci(ci_id)
    if not ci:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Configuration item not found: {ci_id}"
        )
    
    return {"success": True, "data": ci}


@router.post("/cmdb/search")
async def search_configuration_items(request: CMDBSearchRequest):
    """Search for configuration items
    
    Args:
        request: Search criteria
        
    Returns:
        List of matching configuration items
    """
    logger.info(f"POST /cmdb/search: {request.dict()}")
    
    results = cmdb_service.search_cis(
        ci_type=request.ci_type,
        status=request.status,
        environment=request.environment,
        owner=request.owner,
        name=request.name
    )
    
    return {
        "success": True,
        "count": len(results),
        "data": results
    }


@router.get("/cmdb/ci/{ci_id}/dependencies")
async def get_ci_dependencies(ci_id: str):
    """Get dependencies for a configuration item
    
    Args:
        ci_id: Configuration item ID
        
    Returns:
        List of dependent configuration items
    """
    logger.info(f"GET /cmdb/ci/{ci_id}/dependencies")
    
    ci = cmdb_service.get_ci(ci_id)
    if not ci:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Configuration item not found: {ci_id}"
        )
    
    dependencies = cmdb_service.get_dependencies(ci_id)
    
    return {
        "success": True,
        "ci_id": ci_id,
        "count": len(dependencies),
        "data": dependencies
    }


@router.get("/cmdb/ci/{ci_id}/dependents")
async def get_ci_dependents(ci_id: str):
    """Get items that depend on this configuration item
    
    Args:
        ci_id: Configuration item ID
        
    Returns:
        List of configuration items that depend on this CI
    """
    logger.info(f"GET /cmdb/ci/{ci_id}/dependents")
    
    ci = cmdb_service.get_ci(ci_id)
    if not ci:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Configuration item not found: {ci_id}"
        )
    
    dependents = cmdb_service.get_dependents(ci_id)
    
    return {
        "success": True,
        "ci_id": ci_id,
        "count": len(dependents),
        "data": dependents
    }


@router.get("/cmdb/ci/{ci_id}/impact")
async def get_ci_impact_analysis(ci_id: str):
    """Get impact analysis for a configuration item
    
    Args:
        ci_id: Configuration item ID
        
    Returns:
        Impact analysis including all affected items
    """
    logger.info(f"GET /cmdb/ci/{ci_id}/impact")
    
    impact = cmdb_service.get_impact_analysis(ci_id)
    
    if "error" in impact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=impact["error"]
        )
    
    return {
        "success": True,
        "data": impact
    }


@router.get("/cmdb/all")
async def get_all_configuration_items():
    """Get all configuration items
    
    Returns:
        List of all configuration items
    """
    logger.info("GET /cmdb/all")
    
    items = cmdb_service.get_all_cis()
    
    return {
        "success": True,
        "count": len(items),
        "data": items
    }


# ITSM Endpoints
@router.get("/itsm/incident/{incident_id}")
async def get_incident(incident_id: str):
    """Get an incident by ID
    
    Args:
        incident_id: Incident ID
        
    Returns:
        Incident details
    """
    logger.info(f"GET /itsm/incident/{incident_id}")
    
    incident = itsm_service.get_incident(incident_id)
    if not incident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Incident not found: {incident_id}"
        )
    
    return {"success": True, "data": incident}


@router.post("/itsm/incidents/search")
async def search_incidents(request: IncidentSearchRequest):
    """Search for incidents
    
    Args:
        request: Search criteria
        
    Returns:
        List of matching incidents
    """
    logger.info(f"POST /itsm/incidents/search: {request.dict()}")
    
    results = itsm_service.search_incidents(
        priority=request.priority,
        status=request.status,
        affected_ci=request.affected_ci,
        assigned_to=request.assigned_to,
        category=request.category
    )
    
    return {
        "success": True,
        "count": len(results),
        "data": results
    }


@router.get("/itsm/incidents/open")
async def get_open_incidents():
    """Get all open incidents
    
    Returns:
        List of open incidents
    """
    logger.info("GET /itsm/incidents/open")
    
    incidents = itsm_service.get_open_incidents()
    
    return {
        "success": True,
        "count": len(incidents),
        "data": incidents
    }


@router.get("/itsm/change/{change_id}")
async def get_change(change_id: str):
    """Get a change request by ID
    
    Args:
        change_id: Change request ID
        
    Returns:
        Change request details
    """
    logger.info(f"GET /itsm/change/{change_id}")
    
    change = itsm_service.get_change(change_id)
    if not change:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Change request not found: {change_id}"
        )
    
    return {"success": True, "data": change}


@router.post("/itsm/changes/search")
async def search_changes(request: ChangeSearchRequest):
    """Search for change requests
    
    Args:
        request: Search criteria
        
    Returns:
        List of matching change requests
    """
    logger.info(f"POST /itsm/changes/search: {request.dict()}")
    
    results = itsm_service.search_changes(
        change_type=request.change_type,
        status=request.status,
        priority=request.priority,
        affected_ci=request.affected_ci
    )
    
    return {
        "success": True,
        "count": len(results),
        "data": results
    }


@router.get("/itsm/changes/upcoming")
async def get_upcoming_changes():
    """Get all upcoming scheduled changes
    
    Returns:
        List of upcoming changes
    """
    logger.info("GET /itsm/changes/upcoming")
    
    changes = itsm_service.get_upcoming_changes()
    
    return {
        "success": True,
        "count": len(changes),
        "data": changes
    }


@router.get("/itsm/ci/{ci_id}/incidents")
async def get_incidents_for_ci(ci_id: str):
    """Get all incidents for a configuration item
    
    Args:
        ci_id: Configuration item ID
        
    Returns:
        List of incidents affecting this CI
    """
    logger.info(f"GET /itsm/ci/{ci_id}/incidents")
    
    incidents = itsm_service.get_incidents_for_ci(ci_id)
    
    return {
        "success": True,
        "ci_id": ci_id,
        "count": len(incidents),
        "data": incidents
    }


@router.get("/itsm/ci/{ci_id}/changes")
async def get_changes_for_ci(ci_id: str):
    """Get all changes for a configuration item
    
    Args:
        ci_id: Configuration item ID
        
    Returns:
        List of changes affecting this CI
    """
    logger.info(f"GET /itsm/ci/{ci_id}/changes")
    
    changes = itsm_service.get_changes_for_ci(ci_id)
    
    return {
        "success": True,
        "ci_id": ci_id,
        "count": len(changes),
        "data": changes
    }
