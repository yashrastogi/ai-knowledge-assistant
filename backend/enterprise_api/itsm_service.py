"""Mock ITSM (IT Service Management) Service

This module simulates an enterprise ITSM API that manages incidents and changes.
"""
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class ITSMService:
    """Mock ITSM service for incidents and changes"""
    
    def __init__(self):
        """Initialize ITSM with sample data"""
        self.incidents = self._initialize_incident_data()
        self.changes = self._initialize_change_data()
        logger.info(
            f"ITSM initialized with {len(self.incidents)} incidents "
            f"and {len(self.changes)} changes"
        )
    
    def _initialize_incident_data(self) -> Dict[str, Dict[str, Any]]:
        """Create sample incident data
        
        Returns:
            Dictionary of incidents keyed by incident ID
        """
        now = datetime.now()
        return {
            "INC-001": {
                "incident_id": "INC-001",
                "title": "Customer Portal - Slow Response Time",
                "description": "Users reporting slow page load times on customer portal",
                "priority": "P2 - High",
                "status": "In Progress",
                "affected_ci": "APP-001",
                "assigned_to": "Platform Team",
                "reported_by": "Service Desk",
                "created_date": (now - timedelta(hours=2)).isoformat(),
                "updated_date": (now - timedelta(minutes=15)).isoformat(),
                "category": "Performance",
                "impact": "Multiple Users",
                "urgency": "High",
                "resolution_notes": "Investigating database query performance"
            },
            "INC-002": {
                "incident_id": "INC-002",
                "title": "API Gateway - Connection Timeout",
                "description": "API Gateway returning 504 timeout errors intermittently",
                "priority": "P1 - Critical",
                "status": "In Progress",
                "affected_ci": "APP-002",
                "assigned_to": "Platform Team",
                "reported_by": "Monitoring System",
                "created_date": (now - timedelta(hours=1)).isoformat(),
                "updated_date": (now - timedelta(minutes=5)).isoformat(),
                "category": "Availability",
                "impact": "Business Critical",
                "urgency": "Critical",
                "resolution_notes": "Identified Redis cache connectivity issue"
            },
            "INC-003": {
                "incident_id": "INC-003",
                "title": "Dev Server - Disk Space Warning",
                "description": "Development server disk usage at 85%",
                "priority": "P3 - Medium",
                "status": "Open",
                "affected_ci": "SRV-003",
                "assigned_to": "Infrastructure Team",
                "reported_by": "Monitoring System",
                "created_date": (now - timedelta(hours=6)).isoformat(),
                "updated_date": (now - timedelta(hours=6)).isoformat(),
                "category": "Capacity",
                "impact": "Single System",
                "urgency": "Medium",
                "resolution_notes": ""
            },
            "INC-004": {
                "incident_id": "INC-004",
                "title": "Database - Slow Query Performance",
                "description": "PostgreSQL database experiencing slow query performance",
                "priority": "P2 - High",
                "status": "Resolved",
                "affected_ci": "DB-001",
                "assigned_to": "Database Team",
                "reported_by": "Application Team",
                "created_date": (now - timedelta(days=1)).isoformat(),
                "updated_date": (now - timedelta(hours=3)).isoformat(),
                "resolved_date": (now - timedelta(hours=3)).isoformat(),
                "category": "Performance",
                "impact": "Multiple Applications",
                "urgency": "High",
                "resolution_notes": "Optimized indexes and updated statistics"
            },
            "INC-005": {
                "incident_id": "INC-005",
                "title": "Load Balancer - Health Check Failure",
                "description": "Load balancer reporting health check failures on prod-web-01",
                "priority": "P1 - Critical",
                "status": "Resolved",
                "affected_ci": "NET-001",
                "assigned_to": "Network Team",
                "reported_by": "Monitoring System",
                "created_date": (now - timedelta(days=2)).isoformat(),
                "updated_date": (now - timedelta(days=2, hours=-4)).isoformat(),
                "resolved_date": (now - timedelta(days=2, hours=-4)).isoformat(),
                "category": "Availability",
                "impact": "Business Critical",
                "urgency": "Critical",
                "resolution_notes": "Restarted web server service, health checks passing"
            }
        }
    
    def _initialize_change_data(self) -> Dict[str, Dict[str, Any]]:
        """Create sample change request data
        
        Returns:
            Dictionary of changes keyed by change ID
        """
        now = datetime.now()
        return {
            "CHG-001": {
                "change_id": "CHG-001",
                "title": "Upgrade PostgreSQL to 15.4",
                "description": "Security patch upgrade for production PostgreSQL database",
                "type": "Standard",
                "priority": "High",
                "status": "Scheduled",
                "affected_cis": ["DB-001"],
                "requested_by": "Database Team",
                "assigned_to": "Database Team",
                "created_date": (now - timedelta(days=7)).isoformat(),
                "scheduled_start": (now + timedelta(days=2)).isoformat(),
                "scheduled_end": (now + timedelta(days=2, hours=2)).isoformat(),
                "impact_assessment": "Low - Rolling upgrade with minimal downtime",
                "risk_level": "Low",
                "rollback_plan": "Restore from snapshot if issues occur",
                "cab_approval": "Approved",
                "approval_date": (now - timedelta(days=3)).isoformat()
            },
            "CHG-002": {
                "change_id": "CHG-002",
                "title": "Deploy Customer Portal v2.6.0",
                "description": "Deploy new features and bug fixes to customer portal",
                "type": "Standard",
                "priority": "Medium",
                "status": "In Progress",
                "affected_cis": ["APP-001", "SRV-001"],
                "requested_by": "Product Team",
                "assigned_to": "Platform Team",
                "created_date": (now - timedelta(days=5)).isoformat(),
                "scheduled_start": now.isoformat(),
                "scheduled_end": (now + timedelta(hours=1)).isoformat(),
                "impact_assessment": "Medium - 15 minute maintenance window",
                "risk_level": "Medium",
                "rollback_plan": "Revert to v2.5.1 using blue-green deployment",
                "cab_approval": "Approved",
                "approval_date": (now - timedelta(days=2)).isoformat()
            },
            "CHG-003": {
                "change_id": "CHG-003",
                "title": "Scale API Gateway Infrastructure",
                "description": "Add additional instances to handle increased load",
                "type": "Standard",
                "priority": "High",
                "status": "Pending Approval",
                "affected_cis": ["APP-002", "SRV-002"],
                "requested_by": "Platform Team",
                "assigned_to": "Infrastructure Team",
                "created_date": (now - timedelta(days=1)).isoformat(),
                "scheduled_start": (now + timedelta(days=3)).isoformat(),
                "scheduled_end": (now + timedelta(days=3, hours=2)).isoformat(),
                "impact_assessment": "Low - Auto-scaling, no downtime expected",
                "risk_level": "Low",
                "rollback_plan": "Reduce instance count if issues arise",
                "cab_approval": "Pending",
                "approval_date": None
            },
            "CHG-004": {
                "change_id": "CHG-004",
                "title": "Emergency Patch - Redis Security Update",
                "description": "Critical security patch for Redis cache cluster",
                "type": "Emergency",
                "priority": "Critical",
                "status": "Completed",
                "affected_cis": ["DB-002", "APP-002"],
                "requested_by": "Security Team",
                "assigned_to": "Platform Team",
                "created_date": (now - timedelta(days=3)).isoformat(),
                "scheduled_start": (now - timedelta(days=3, hours=-1)).isoformat(),
                "scheduled_end": (now - timedelta(days=3, hours=-1, minutes=-30)).isoformat(),
                "completed_date": (now - timedelta(days=3, hours=-1, minutes=-25)).isoformat(),
                "impact_assessment": "High - Requires cluster restart",
                "risk_level": "High",
                "rollback_plan": "Snapshot available for rollback",
                "cab_approval": "Emergency Approved",
                "approval_date": (now - timedelta(days=3, hours=-2)).isoformat()
            }
        }
    
    def get_incident(self, incident_id: str) -> Optional[Dict[str, Any]]:
        """Get an incident by ID
        
        Args:
            incident_id: Incident ID
            
        Returns:
            Incident details or None if not found
        """
        incident = self.incidents.get(incident_id)
        if incident:
            logger.info(f"Retrieved incident: {incident_id}")
        else:
            logger.warning(f"Incident not found: {incident_id}")
        return incident
    
    def search_incidents(
        self,
        priority: Optional[str] = None,
        status: Optional[str] = None,
        affected_ci: Optional[str] = None,
        assigned_to: Optional[str] = None,
        category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Search incidents by criteria
        
        Args:
            priority: Filter by priority (P1, P2, P3, P4)
            status: Filter by status (Open, In Progress, Resolved)
            affected_ci: Filter by affected configuration item
            assigned_to: Filter by assigned team
            category: Filter by category
            
        Returns:
            List of matching incidents
        """
        results = list(self.incidents.values())
        
        if priority:
            results = [inc for inc in results if inc.get("priority") == priority]
        
        if status:
            results = [inc for inc in results if inc.get("status") == status]
        
        if affected_ci:
            results = [inc for inc in results if inc.get("affected_ci") == affected_ci]
        
        if assigned_to:
            results = [inc for inc in results if inc.get("assigned_to") == assigned_to]
        
        if category:
            results = [inc for inc in results if inc.get("category") == category]
        
        logger.info(f"Incident search returned {len(results)} results")
        return results
    
    def get_open_incidents(self) -> List[Dict[str, Any]]:
        """Get all open incidents
        
        Returns:
            List of open incidents
        """
        return self.search_incidents(status="Open") + self.search_incidents(status="In Progress")
    
    def get_change(self, change_id: str) -> Optional[Dict[str, Any]]:
        """Get a change request by ID
        
        Args:
            change_id: Change request ID
            
        Returns:
            Change request details or None if not found
        """
        change = self.changes.get(change_id)
        if change:
            logger.info(f"Retrieved change: {change_id}")
        else:
            logger.warning(f"Change not found: {change_id}")
        return change
    
    def search_changes(
        self,
        change_type: Optional[str] = None,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        affected_ci: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Search change requests by criteria
        
        Args:
            change_type: Filter by type (Standard, Emergency, Normal)
            status: Filter by status (Pending, Scheduled, In Progress, Completed)
            priority: Filter by priority
            affected_ci: Filter by affected configuration item
            
        Returns:
            List of matching change requests
        """
        results = list(self.changes.values())
        
        if change_type:
            results = [chg for chg in results if chg.get("type") == change_type]
        
        if status:
            results = [chg for chg in results if chg.get("status") == status]
        
        if priority:
            results = [chg for chg in results if chg.get("priority") == priority]
        
        if affected_ci:
            results = [
                chg for chg in results 
                if affected_ci in chg.get("affected_cis", [])
            ]
        
        logger.info(f"Change search returned {len(results)} results")
        return results
    
    def get_upcoming_changes(self) -> List[Dict[str, Any]]:
        """Get all upcoming scheduled changes
        
        Returns:
            List of scheduled and in-progress changes
        """
        return (
            self.search_changes(status="Scheduled") + 
            self.search_changes(status="In Progress")
        )
    
    def get_incidents_for_ci(self, ci_id: str) -> List[Dict[str, Any]]:
        """Get all incidents related to a configuration item
        
        Args:
            ci_id: Configuration item ID
            
        Returns:
            List of related incidents
        """
        return self.search_incidents(affected_ci=ci_id)
    
    def get_changes_for_ci(self, ci_id: str) -> List[Dict[str, Any]]:
        """Get all changes related to a configuration item
        
        Args:
            ci_id: Configuration item ID
            
        Returns:
            List of related changes
        """
        return self.search_changes(affected_ci=ci_id)


# Global ITSM service instance
itsm_service = ITSMService()
