"""Multi-agent system for advanced RAG workflows"""
from typing import List, Dict, Any, Optional
import logging
from langchain.agents import AgentExecutor, create_react_agent
from langchain.agents import Tool
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import Document
from retrieval import retrieval_service
from config import settings
from enterprise_api import cmdb_service, itsm_service

logger = logging.getLogger(__name__)


class RetrieverAgent:
    """Agent specialized in retrieving relevant documents"""
    
    def __init__(self):
        """Initialize retriever agent"""
        self.name = "Retriever"
        self.description = "Retrieves relevant documents from the knowledge base"
    
    def retrieve(self, query: str, k: int = 4) -> List[Document]:
        """Retrieve documents for a query
        
        Args:
            query: Search query
            k: Number of documents to retrieve
            
        Returns:
            List of relevant documents
        """
        logger.info(f"[{self.name}] Retrieving documents for: {query}")
        
        if not retrieval_service.is_ready():
            logger.error(f"[{self.name}] Retrieval service not ready")
            return []
        
        try:
            results = retrieval_service.retrieve(
                query=query,
                k=k,
                use_hybrid=False
            )
            logger.info(f"[{self.name}] Retrieved {len(results)} documents")
            return results
        except Exception as e:
            logger.error(f"[{self.name}] Error retrieving documents: {e}")
            return []
    
    def retrieve_with_scores(self, query: str, k: int = 4) -> List[tuple[Document, float]]:
        """Retrieve documents with relevance scores
        
        Args:
            query: Search query
            k: Number of documents to retrieve
            
        Returns:
            List of (document, score) tuples
        """
        logger.info(f"[{self.name}] Retrieving documents with scores for: {query}")
        
        if not retrieval_service.is_ready():
            logger.error(f"[{self.name}] Retrieval service not ready")
            return []
        
        try:
            results = retrieval_service.retrieve_with_scores(
                query=query,
                k=k
            )
            logger.info(f"[{self.name}] Retrieved {len(results)} documents with scores")
            return results
        except Exception as e:
            logger.error(f"[{self.name}] Error retrieving documents: {e}")
            return []


class SynthesizerAgent:
    """Agent specialized in synthesizing information from multiple sources"""
    
    def __init__(self, llm: Optional[ChatGoogleGenerativeAI] = None):
        """Initialize synthesizer agent
        
        Args:
            llm: Language model for synthesis
        """
        self.name = "Synthesizer"
        self.description = "Synthesizes information from multiple documents into coherent answers"
        self.llm = llm or ChatGoogleGenerativeAI(
            model=settings.gemini_model,
            google_api_key=settings.google_api_key,
            temperature=0.5
        )
    
    def synthesize(
        self,
        question: str,
        documents: List[Document],
        context: Optional[str] = None
    ) -> str:
        """Synthesize answer from documents
        
        Args:
            question: User's question
            documents: Source documents
            context: Optional additional context
            
        Returns:
            Synthesized answer
        """
        logger.info(f"[{self.name}] Synthesizing answer from {len(documents)} documents")
        
        if not documents:
            return "No relevant information found in the knowledge base."
        
        # Prepare context from documents
        doc_context = "\n\n".join([
            f"Document {i+1}:\n{doc.page_content}"
            for i, doc in enumerate(documents)
        ])
        
        # Create synthesis prompt
        prompt = f"""You are an expert at synthesizing information from multiple sources.

Question: {question}

Source Documents:
{doc_context}

{f"Additional Context: {context}" if context else ""}

Task: Provide a comprehensive, accurate answer based on the source documents. 
- Synthesize information from all relevant sources
- Maintain factual accuracy
- Cite which documents support your statements (e.g., "According to Document 1...")
- If documents contain conflicting information, acknowledge it
- Use clear, professional language

Answer:"""
        
        try:
            response = self.llm.invoke(prompt)
            answer = response.content if hasattr(response, 'content') else str(response)
            logger.info(f"[{self.name}] Generated synthesized answer")
            return answer
        except Exception as e:
            logger.error(f"[{self.name}] Error synthesizing answer: {e}")
            return f"Error synthesizing answer: {str(e)}"


class EnterpriseAPIAgent:
    """Agent specialized in querying enterprise CMDB and ITSM APIs"""
    
    def __init__(self):
        """Initialize enterprise API agent"""
        self.name = "EnterpriseAPI"
        self.description = "Queries CMDB and ITSM systems for configuration items, incidents, and changes"
        self.cmdb = cmdb_service
        self.itsm = itsm_service
    
    def query_cmdb(
        self,
        query_type: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Query CMDB for configuration items
        
        Args:
            query_type: Type of query (get_ci, search_cis, get_dependencies, etc.)
            **kwargs: Query parameters
            
        Returns:
            Query results
        """
        logger.info(f"[{self.name}] CMDB query: {query_type}")
        
        try:
            if query_type == "get_ci":
                result = self.cmdb.get_ci(kwargs.get("ci_id"))
            elif query_type == "search_cis":
                result = self.cmdb.search_cis(**kwargs)
            elif query_type == "get_dependencies":
                result = self.cmdb.get_dependencies(kwargs.get("ci_id"))
            elif query_type == "get_dependents":
                result = self.cmdb.get_dependents(kwargs.get("ci_id"))
            elif query_type == "get_impact_analysis":
                result = self.cmdb.get_impact_analysis(kwargs.get("ci_id"))
            elif query_type == "get_all":
                result = self.cmdb.get_all_cis()
            else:
                result = {"error": f"Unknown query type: {query_type}"}
            
            logger.info(f"[{self.name}] CMDB query returned results")
            return {"success": True, "data": result}
            
        except Exception as e:
            logger.error(f"[{self.name}] CMDB query error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def query_itsm(
        self,
        query_type: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Query ITSM for incidents and changes
        
        Args:
            query_type: Type of query (get_incident, search_incidents, etc.)
            **kwargs: Query parameters
            
        Returns:
            Query results
        """
        logger.info(f"[{self.name}] ITSM query: {query_type}")
        
        try:
            if query_type == "get_incident":
                result = self.itsm.get_incident(kwargs.get("incident_id"))
            elif query_type == "search_incidents":
                result = self.itsm.search_incidents(**kwargs)
            elif query_type == "get_open_incidents":
                result = self.itsm.get_open_incidents()
            elif query_type == "get_change":
                result = self.itsm.get_change(kwargs.get("change_id"))
            elif query_type == "search_changes":
                result = self.itsm.search_changes(**kwargs)
            elif query_type == "get_upcoming_changes":
                result = self.itsm.get_upcoming_changes()
            elif query_type == "get_incidents_for_ci":
                result = self.itsm.get_incidents_for_ci(kwargs.get("ci_id"))
            elif query_type == "get_changes_for_ci":
                result = self.itsm.get_changes_for_ci(kwargs.get("ci_id"))
            else:
                result = {"error": f"Unknown query type: {query_type}"}
            
            logger.info(f"[{self.name}] ITSM query returned results")
            return {"success": True, "data": result}
            
        except Exception as e:
            logger.error(f"[{self.name}] ITSM query error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def format_for_context(self, data: Any, data_type: str) -> str:
        """Format API results for use as context in synthesis
        
        Args:
            data: API response data
            data_type: Type of data (ci, incident, change, etc.)
            
        Returns:
            Formatted string for context
        """
        if not data:
            return "No data found."
        
        if isinstance(data, list):
            if len(data) == 0:
                return "No results found."
            return "\n\n".join([self._format_single_item(item, data_type) for item in data])
        else:
            return self._format_single_item(data, data_type)
    
    def _format_single_item(self, item: Dict[str, Any], data_type: str) -> str:
        """Format a single item for context
        
        Args:
            item: Data item
            data_type: Type of data
            
        Returns:
            Formatted string
        """
        if data_type == "ci":
            return (
                f"Configuration Item: {item.get('name', 'Unknown')}\n"
                f"  ID: {item.get('ci_id')}\n"
                f"  Type: {item.get('ci_type')}\n"
                f"  Status: {item.get('status')}\n"
                f"  Environment: {item.get('environment')}\n"
                f"  Owner: {item.get('owner')}\n"
                f"  Location: {item.get('location', 'N/A')}"
            )
        elif data_type == "incident":
            return (
                f"Incident: {item.get('title', 'Unknown')}\n"
                f"  ID: {item.get('incident_id')}\n"
                f"  Priority: {item.get('priority')}\n"
                f"  Status: {item.get('status')}\n"
                f"  Affected CI: {item.get('affected_ci')}\n"
                f"  Assigned To: {item.get('assigned_to')}\n"
                f"  Description: {item.get('description', 'N/A')}"
            )
        elif data_type == "change":
            return (
                f"Change Request: {item.get('title', 'Unknown')}\n"
                f"  ID: {item.get('change_id')}\n"
                f"  Type: {item.get('type')}\n"
                f"  Status: {item.get('status')}\n"
                f"  Priority: {item.get('priority')}\n"
                f"  Affected CIs: {', '.join(item.get('affected_cis', []))}\n"
                f"  Scheduled: {item.get('scheduled_start', 'N/A')}"
            )
        else:
            return str(item)


class ValidatorAgent:
    """Agent specialized in validating answer quality and relevance"""
    
    def __init__(self, llm: Optional[ChatGoogleGenerativeAI] = None):
        """Initialize validator agent
        
        Args:
            llm: Language model for validation
        """
        self.name = "Validator"
        self.description = "Validates answer quality, relevance, and accuracy"
        self.llm = llm or ChatGoogleGenerativeAI(
            model=settings.gemini_model,
            google_api_key=settings.google_api_key,
            temperature=0.2
        )
    
    def validate(
        self,
        question: str,
        answer: str,
        documents: List[Document]
    ) -> Dict[str, Any]:
        """Validate an answer
        
        Args:
            question: Original question
            answer: Generated answer
            documents: Source documents used
            
        Returns:
            Validation result with scores and feedback
        """
        logger.info(f"[{self.name}] Validating answer")
        
        # Prepare document context
        doc_context = "\n".join([
            f"- {doc.page_content[:200]}..."
            for doc in documents[:3]  # Use first 3 docs for validation
        ])
        
        # Create validation prompt
        prompt = f"""You are an expert at validating AI-generated answers.

Question: {question}

Generated Answer:
{answer}

Source Documents Used:
{doc_context}

Evaluate this answer on the following criteria (rate each 1-10):
1. RELEVANCE: Does the answer address the question?
2. ACCURACY: Is the answer factually correct based on the sources?
3. COMPLETENESS: Does it cover important aspects?
4. CLARITY: Is it well-written and easy to understand?

Provide your evaluation in this exact format:
RELEVANCE: [score]
ACCURACY: [score]
COMPLETENESS: [score]
CLARITY: [score]
OVERALL: [average score]
FEEDBACK: [Brief explanation of scores and any concerns]

Evaluation:"""
        
        try:
            response = self.llm.invoke(prompt)
            validation_text = response.content if hasattr(response, 'content') else str(response)
            
            # Parse validation response
            validation_result = self._parse_validation(validation_text)
            logger.info(f"[{self.name}] Validation complete - Overall: {validation_result.get('overall', 0)}/10")
            
            return validation_result
            
        except Exception as e:
            logger.error(f"[{self.name}] Error validating answer: {e}")
            return {
                "relevance": 5,
                "accuracy": 5,
                "completeness": 5,
                "clarity": 5,
                "overall": 5,
                "feedback": f"Validation error: {str(e)}",
                "passed": True
            }
    
    def _parse_validation(self, validation_text: str) -> Dict[str, Any]:
        """Parse validation response into structured format"""
        result = {
            "relevance": 0,
            "accuracy": 0,
            "completeness": 0,
            "clarity": 0,
            "overall": 0,
            "feedback": "",
            "passed": False
        }
        
        lines = validation_text.strip().split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('RELEVANCE:'):
                try:
                    result["relevance"] = float(line.split(':')[1].strip())
                except:
                    pass
            elif line.startswith('ACCURACY:'):
                try:
                    result["accuracy"] = float(line.split(':')[1].strip())
                except:
                    pass
            elif line.startswith('COMPLETENESS:'):
                try:
                    result["completeness"] = float(line.split(':')[1].strip())
                except:
                    pass
            elif line.startswith('CLARITY:'):
                try:
                    result["clarity"] = float(line.split(':')[1].strip())
                except:
                    pass
            elif line.startswith('OVERALL:'):
                try:
                    result["overall"] = float(line.split(':')[1].strip())
                except:
                    pass
            elif line.startswith('FEEDBACK:'):
                result["feedback"] = line.split(':', 1)[1].strip()
        
        # Consider answer passed if overall score >= 7
        result["passed"] = result["overall"] >= 7.0
        
        return result


class MultiAgentOrchestrator:
    """Orchestrates multiple agents for complex Q&A workflows"""
    
    def __init__(self):
        """Initialize orchestrator with all agents"""
        self.retriever = RetrieverAgent()
        self.synthesizer = SynthesizerAgent()
        self.validator = ValidatorAgent()
        self.enterprise_api = EnterpriseAPIAgent()
        self._initialized = False
    
    def initialize(self) -> None:
        """Initialize the orchestrator"""
        if self._initialized:
            logger.info("Multi-agent orchestrator already initialized")
            return
        
        logger.info("Initializing multi-agent orchestrator...")
        
        if not retrieval_service.is_ready():
            raise RuntimeError("Retrieval service not ready")
        
        self._initialized = True
        logger.info("Multi-agent orchestrator initialized successfully")
    
    def is_ready(self) -> bool:
        """Check if orchestrator is ready"""
        return self._initialized
    
    def _should_use_enterprise_api(self, question: str) -> bool:
        """Determine if enterprise APIs should be queried
        
        Args:
            question: User's question
            
        Returns:
            True if enterprise APIs should be used
        """
        # Keywords that suggest operational queries
        operational_keywords = [
            'incident', 'outage', 'down', 'issue', 'problem',
            'server', 'ci', 'configuration', 'change', 'ticket',
            'status', 'affected', 'impact', 'dependency'
        ]
        
        question_lower = question.lower()
        return any(keyword in question_lower for keyword in operational_keywords)
    
    def process_query(
        self,
        question: str,
        k: int = 4,
        validate: bool = True,
        use_enterprise_api: bool = False
    ) -> Dict[str, Any]:
        """Process a query using multi-agent workflow
        
        Args:
            question: User's question
            k: Number of documents to retrieve
            validate: Whether to validate the answer
            use_enterprise_api: Whether to query enterprise APIs (auto-detect if None)
            
        Returns:
            Complete result with answer, sources, and validation
        """
        if not self.is_ready():
            raise RuntimeError("Multi-agent orchestrator not initialized")
        
        logger.info(f"[Orchestrator] Processing query with {k} documents")
        
        try:
            # Auto-detect if we should use enterprise API
            if use_enterprise_api is None:
                use_enterprise_api = self._should_use_enterprise_api(question)
            
            agent_workflow = []
            additional_context = None
            
            # Step 1: Retrieval from knowledge base
            documents = self.retriever.retrieve(question, k=k)
            agent_workflow.append("retriever")
            
            # Step 1b: Query enterprise APIs if relevant
            if use_enterprise_api:
                enterprise_context = self._query_enterprise_context(question)
                if enterprise_context:
                    additional_context = enterprise_context
                    agent_workflow.append("enterprise_api")
            
            if not documents and not additional_context:
                return {
                    "question": question,
                    "answer": "No relevant information found in the knowledge base or operational systems.",
                    "source_documents": [],
                    "enterprise_data": None,
                    "validation": None,
                    "success": True,
                    "agent_workflow": agent_workflow
                }
            
            # Step 2: Synthesis
            answer = self.synthesizer.synthesize(
                question, 
                documents,
                context=additional_context
            )
            agent_workflow.append("synthesizer")
            
            result = {
                "question": question,
                "answer": answer,
                "source_documents": [
                    {
                        "content": doc.page_content,
                        "metadata": doc.metadata,
                        "preview": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
                    }
                    for doc in documents
                ],
                "enterprise_data": additional_context if use_enterprise_api else None,
                "validation": None,
                "success": True,
                "agent_workflow": agent_workflow
            }
            
            # Step 3: Validation (optional)
            if validate:
                validation = self.validator.validate(question, answer, documents)
                result["validation"] = validation
                result["agent_workflow"].append("validator")
                
                # If validation fails, add warning
                if not validation.get("passed", True):
                    result["warning"] = "Answer validation score is low. Please verify the information."
            
            logger.info(f"[Orchestrator] Query processed successfully using {len(result['agent_workflow'])} agents")
            return result
            
        except Exception as e:
            logger.error(f"[Orchestrator] Error processing query: {e}")
            return {
                "question": question,
                "answer": f"Error processing query: {str(e)}",
                "source_documents": [],
                "enterprise_data": None,
                "validation": None,
                "success": False,
                "error": str(e),
                "agent_workflow": []
            }
    
    def _query_enterprise_context(self, question: str) -> Optional[str]:
        """Query enterprise APIs for additional context
        
        Args:
            question: User's question
            
        Returns:
            Formatted context from enterprise systems
        """
        logger.info(f"[Orchestrator] Querying enterprise APIs for context")
        
        context_parts = []
        question_lower = question.lower()
        
        # Query incidents if relevant
        if any(kw in question_lower for kw in ['incident', 'issue', 'outage', 'down', 'problem']):
            incidents = self.enterprise_api.query_itsm("get_open_incidents")
            if incidents.get("success") and incidents.get("data"):
                formatted = self.enterprise_api.format_for_context(
                    incidents["data"], "incident"
                )
                context_parts.append(f"Open Incidents:\n{formatted}")
        
        # Query CIs if relevant
        if any(kw in question_lower for kw in ['server', 'ci', 'configuration', 'system']):
            cis = self.enterprise_api.query_cmdb("get_all")
            if cis.get("success") and cis.get("data"):
                # Limit to 5 CIs for context
                ci_data = cis["data"][:5] if isinstance(cis["data"], list) else [cis["data"]]
                formatted = self.enterprise_api.format_for_context(ci_data, "ci")
                context_parts.append(f"Configuration Items:\n{formatted}")
        
        # Query changes if relevant
        if any(kw in question_lower for kw in ['change', 'maintenance', 'scheduled']):
            changes = self.enterprise_api.query_itsm("get_upcoming_changes")
            if changes.get("success") and changes.get("data"):
                formatted = self.enterprise_api.format_for_context(
                    changes["data"], "change"
                )
                context_parts.append(f"Upcoming Changes:\n{formatted}")
        
        if context_parts:
            return "\n\n".join(context_parts)
        
        return None


# Global orchestrator instance (initialized lazily)
_multi_agent_orchestrator = None

def get_multi_agent_orchestrator() -> MultiAgentOrchestrator:
    """Get or create the global multi-agent orchestrator instance"""
    global _multi_agent_orchestrator
    if _multi_agent_orchestrator is None:
        _multi_agent_orchestrator = MultiAgentOrchestrator()
    return _multi_agent_orchestrator

# For backward compatibility
multi_agent_orchestrator = None  # Will be initialized when first accessed
