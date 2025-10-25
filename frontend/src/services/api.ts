/**
 * API Service for communicating with the backend
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface QueryRequest {
  question: string;
  k?: number;
  return_sources?: boolean;
  use_multi_agent?: boolean;
  validate_answer?: boolean;
  use_enterprise_api?: boolean;
}

export interface SourceDocument {
  content: string;
  preview: string;
  metadata: Record<string, unknown>;
}

export interface ValidationScores {
  relevance: number;
  accuracy: number;
  completeness: number;
  clarity: number;
  overall: number;
  feedback: string;
  passed: boolean;
}

export interface QueryResponse {
  answer: string;
  question: string;
  success: boolean;
  source_documents?: SourceDocument[];
  enterprise_data?: string;
  validation?: ValidationScores;
  agent_workflow?: string[];
  warning?: string;
  error?: string;
}

export interface HealthResponse {
  status: string;
}

export interface StatusResponse {
  status: string;
  services: {
    api: string;
    vector_store: string;
    rag_chain: string;
    multi_agent: string;
  };
}

class ApiService {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  /**
   * Check if the backend is healthy
   */
  async checkHealth(): Promise<HealthResponse> {
    const response = await fetch(`${this.baseUrl}/health`);
    if (!response.ok) {
      throw new Error('Health check failed');
    }
    return response.json();
  }

  /**
   * Get system status
   */
  async getStatus(): Promise<StatusResponse> {
    const response = await fetch(`${this.baseUrl}/status`);
    if (!response.ok) {
      throw new Error('Status check failed');
    }
    return response.json();
  }

  /**
   * Query the knowledge base
   */
  async query(request: QueryRequest): Promise<QueryResponse> {
    const response = await fetch(`${this.baseUrl}/api/v1/query`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Query failed');
    }

    return response.json();
  }
}

export const apiService = new ApiService();
