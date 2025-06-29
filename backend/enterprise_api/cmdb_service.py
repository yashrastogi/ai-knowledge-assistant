"""Mock CMDB (Configuration Management Database) Service

This module simulates an enterprise CMDB API that stores and manages
configuration items (CIs) including servers, applications, and their relationships.
"""
from typing import List, Dict, Optional, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class CMDBService:
    """Mock CMDB service for configuration items"""
    
    def __init__(self):
        """Initialize CMDB with sample data"""
        self.configuration_items = self._initialize_sample_data()
        logger.info(f"CMDB initialized with {len(self.configuration_items)} configuration items")
    
    def _initialize_sample_data(self) -> Dict[str, Dict[str, Any]]:
        """Create sample CMDB data
        
        Returns:
            Dictionary of configuration items keyed by CI ID
        """
        return {
            # Servers
            "SRV-001": {
                "ci_id": "SRV-001",
                "ci_type": "Server",
                "name": "prod-web-01",
                "status": "Active",
                "environment": "Production",
                "location": "AWS US-East-1",
                "owner": "Platform Team",
                "specs": {
                    "cpu": "8 cores",
                    "memory": "32 GB",
                    "storage": "500 GB SSD",
                    "os": "Ubuntu 22.04 LTS"
                },
                "dependencies": ["APP-001", "DB-001"],
                "created_date": "2024-01-15",
                "last_updated": "2025-10-20"
            },
            "SRV-002": {
                "ci_id": "SRV-002",
                "ci_type": "Server",
                "name": "prod-api-01",
                "status": "Active",
                "environment": "Production",
                "location": "AWS US-East-1",
                "owner": "Platform Team",
                "specs": {
                    "cpu": "16 cores",
                    "memory": "64 GB",
                    "storage": "1 TB SSD",
                    "os": "Ubuntu 22.04 LTS"
                },
                "dependencies": ["APP-002", "DB-001"],
                "created_date": "2024-02-10",
                "last_updated": "2025-10-18"
            },
            "SRV-003": {
                "ci_id": "SRV-003",
                "ci_type": "Server",
                "name": "dev-test-01",
                "status": "Active",
                "environment": "Development",
                "location": "AWS US-West-2",
                "owner": "Development Team",
                "specs": {
                    "cpu": "4 cores",
                    "memory": "16 GB",
                    "storage": "200 GB SSD",
                    "os": "Ubuntu 22.04 LTS"
                },
                "dependencies": ["APP-001"],
                "created_date": "2024-03-01",
                "last_updated": "2025-10-15"
            },
            
            # Applications
            "APP-001": {
                "ci_id": "APP-001",
                "ci_type": "Application",
                "name": "Customer Portal",
                "status": "Active",
                "environment": "Production",
                "version": "2.5.1",
                "owner": "Product Team",
                "tech_stack": ["React", "Node.js", "PostgreSQL"],
                "dependencies": ["DB-001", "API-001"],
                "created_date": "2023-06-01",
                "last_updated": "2025-10-21"
            },
            "APP-002": {
                "ci_id": "APP-002",
                "ci_type": "Application",
                "name": "Internal API Gateway",
                "status": "Active",
                "environment": "Production",
                "version": "3.2.0",
                "owner": "Platform Team",
                "tech_stack": ["FastAPI", "Python", "Redis"],
                "dependencies": ["DB-001", "DB-002"],
                "created_date": "2023-08-15",
                "last_updated": "2025-10-22"
            },
            
            # Databases
            "DB-001": {
                "ci_id": "DB-001",
                "ci_type": "Database",
                "name": "prod-postgres-primary",
                "status": "Active",
                "environment": "Production",
                "db_type": "PostgreSQL",
                "version": "15.3",
                "location": "AWS RDS US-East-1",
                "owner": "Database Team",
                "specs": {
                    "instance_type": "db.r6g.2xlarge",
                    "storage": "2 TB",
                    "backup": "Daily",
                    "multi_az": True
                },
                "dependencies": [],
                "created_date": "2023-05-01",
                "last_updated": "2025-10-19"
            },
            "DB-002": {
                "ci_id": "DB-002",
                "ci_type": "Database",
                "name": "redis-cache-cluster",
                "status": "Active",
                "environment": "Production",
                "db_type": "Redis",
                "version": "7.0",
                "location": "AWS ElastiCache US-East-1",
                "owner": "Platform Team",
                "specs": {
                    "instance_type": "cache.r6g.large",
                    "nodes": 3,
                    "memory": "26 GB"
                },
                "dependencies": [],
                "created_date": "2023-07-01",
                "last_updated": "2025-10-20"
            },
            
            # Network Devices
            "NET-001": {
                "ci_id": "NET-001",
                "ci_type": "Network Device",
                "name": "prod-load-balancer",
                "status": "Active",
                "environment": "Production",
                "device_type": "Application Load Balancer",
                "location": "AWS US-East-1",
                "owner": "Network Team",
                "dependencies": ["SRV-001", "SRV-002"],
                "created_date": "2023-05-15",
                "last_updated": "2025-10-21"
            }
        }
    
    def get_ci(self, ci_id: str) -> Optional[Dict[str, Any]]:
        """Get a configuration item by ID
        
        Args:
            ci_id: Configuration item ID
            
        Returns:
            Configuration item details or None if not found
        """
        ci = self.configuration_items.get(ci_id)
        if ci:
            logger.info(f"Retrieved CI: {ci_id}")
        else:
            logger.warning(f"CI not found: {ci_id}")
        return ci
    
    def search_cis(
        self,
        ci_type: Optional[str] = None,
        status: Optional[str] = None,
        environment: Optional[str] = None,
        owner: Optional[str] = None,
        name: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Search configuration items by criteria
        
        Args:
            ci_type: Filter by CI type (Server, Application, Database, etc.)
            status: Filter by status (Active, Inactive, Maintenance)
            environment: Filter by environment (Production, Development, etc.)
            owner: Filter by owner team
            name: Filter by name (partial match)
            
        Returns:
            List of matching configuration items
        """
        results = list(self.configuration_items.values())
        
        if ci_type:
            results = [ci for ci in results if ci.get("ci_type") == ci_type]
        
        if status:
            results = [ci for ci in results if ci.get("status") == status]
        
        if environment:
            results = [ci for ci in results if ci.get("environment") == environment]
        
        if owner:
            results = [ci for ci in results if ci.get("owner") == owner]
        
        if name:
            results = [ci for ci in results if name.lower() in ci.get("name", "").lower()]
        
        logger.info(f"CMDB search returned {len(results)} results")
        return results
    
    def get_dependencies(self, ci_id: str) -> List[Dict[str, Any]]:
        """Get all dependencies for a configuration item
        
        Args:
            ci_id: Configuration item ID
            
        Returns:
            List of dependent configuration items
        """
        ci = self.get_ci(ci_id)
        if not ci:
            return []
        
        dependency_ids = ci.get("dependencies", [])
        dependencies = []
        
        for dep_id in dependency_ids:
            dep_ci = self.get_ci(dep_id)
            if dep_ci:
                dependencies.append(dep_ci)
        
        logger.info(f"Found {len(dependencies)} dependencies for {ci_id}")
        return dependencies
    
    def get_dependents(self, ci_id: str) -> List[Dict[str, Any]]:
        """Get all CIs that depend on this configuration item
        
        Args:
            ci_id: Configuration item ID
            
        Returns:
            List of configuration items that depend on this CI
        """
        dependents = []
        
        for ci in self.configuration_items.values():
            if ci_id in ci.get("dependencies", []):
                dependents.append(ci)
        
        logger.info(f"Found {len(dependents)} dependents for {ci_id}")
        return dependents
    
    def get_all_cis(self) -> List[Dict[str, Any]]:
        """Get all configuration items
        
        Returns:
            List of all configuration items
        """
        return list(self.configuration_items.values())
    
    def get_impact_analysis(self, ci_id: str) -> Dict[str, Any]:
        """Get impact analysis for a configuration item
        
        Args:
            ci_id: Configuration item ID
            
        Returns:
            Impact analysis including direct and indirect dependencies
        """
        ci = self.get_ci(ci_id)
        if not ci:
            return {"error": f"CI not found: {ci_id}"}
        
        # Get direct dependencies
        direct_deps = self.get_dependencies(ci_id)
        
        # Get direct dependents
        direct_dependents = self.get_dependents(ci_id)
        
        # Get indirect dependents (things that depend on our dependents)
        indirect_dependents = []
        seen_ids = set()
        for dependent in direct_dependents:
            indirect = self.get_dependents(dependent["ci_id"])
            for item in indirect:
                if item["ci_id"] not in seen_ids:
                    seen_ids.add(item["ci_id"])
                    indirect_dependents.append(item)
        
        impact_analysis = {
            "ci": ci,
            "direct_dependencies": direct_deps,
            "direct_dependents": direct_dependents,
            "indirect_dependents": indirect_dependents,
            "total_impact": len(direct_dependents) + len(indirect_dependents),
            "risk_level": self._calculate_risk_level(
                len(direct_dependents) + len(indirect_dependents),
                ci.get("environment", "")
            )
        }
        
        logger.info(f"Impact analysis for {ci_id}: {impact_analysis['total_impact']} items affected")
        return impact_analysis
    
    def _calculate_risk_level(self, impact_count: int, environment: str) -> str:
        """Calculate risk level based on impact and environment
        
        Args:
            impact_count: Number of items affected
            environment: Environment type
            
        Returns:
            Risk level string
        """
        if environment == "Production":
            if impact_count >= 5:
                return "Critical"
            elif impact_count >= 3:
                return "High"
            elif impact_count >= 1:
                return "Medium"
        else:
            if impact_count >= 10:
                return "High"
            elif impact_count >= 5:
                return "Medium"
        
        return "Low"


# Global CMDB service instance
cmdb_service = CMDBService()
