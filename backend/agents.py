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
    
    def process_query(
        self,
        question: str,
        k: int = 4,
        validate: bool = True
    ) -> Dict[str, Any]:
        """Process a query using multi-agent workflow
        
        Args:
            question: User's question
            k: Number of documents to retrieve
            validate: Whether to validate the answer
            
        Returns:
            Complete result with answer, sources, and validation
        """
        if not self.is_ready():
            raise RuntimeError("Multi-agent orchestrator not initialized")
        
        logger.info(f"[Orchestrator] Processing query with {k} documents")
        
        try:
            # Step 1: Retrieval
            documents = self.retriever.retrieve(question, k=k)
            
            if not documents:
                return {
                    "question": question,
                    "answer": "No relevant information found in the knowledge base.",
                    "source_documents": [],
                    "validation": None,
                    "success": True,
                    "agent_workflow": ["retriever"]
                }
            
            # Step 2: Synthesis
            answer = self.synthesizer.synthesize(question, documents)
            
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
                "validation": None,
                "success": True,
                "agent_workflow": ["retriever", "synthesizer"]
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
                "validation": None,
                "success": False,
                "error": str(e),
                "agent_workflow": []
            }


# Global orchestrator instance
multi_agent_orchestrator = MultiAgentOrchestrator()
