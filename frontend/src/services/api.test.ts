import { describe, it, expect, beforeEach, vi } from 'vitest';
import { apiService } from './api';

// Mock fetch globally
globalThis.fetch = vi.fn() as typeof fetch;

describe('ApiService', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('checkHealth', () => {
    it('should return health status on success', async () => {
      const mockResponse = { status: 'healthy' };
      (globalThis.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const result = await apiService.checkHealth();
      
      expect(result).toEqual(mockResponse);
      expect(globalThis.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/health')
      );
    });

    it('should throw error on failed health check', async () => {
      (globalThis.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
        ok: false,
      });

      await expect(apiService.checkHealth()).rejects.toThrow('Health check failed');
    });
  });

  describe('getStatus', () => {
    it('should return system status on success', async () => {
      const mockResponse = {
        status: 'operational',
        services: {
          api: 'running',
          vector_store: 'running',
          rag_chain: 'running',
          multi_agent: 'running',
        },
      };
      (globalThis.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const result = await apiService.getStatus();
      
      expect(result).toEqual(mockResponse);
      expect(globalThis.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/status')
      );
    });

    it('should throw error on failed status check', async () => {
      (globalThis.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
        ok: false,
      });

      await expect(apiService.getStatus()).rejects.toThrow('Status check failed');
    });
  });

  describe('query', () => {
    it('should return query response on success', async () => {
      const mockRequest = {
        question: 'What is AI?',
        k: 3,
      };
      const mockResponse = {
        answer: 'AI stands for Artificial Intelligence',
        question: 'What is AI?',
        success: true,
      };
      
      (globalThis.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const result = await apiService.query(mockRequest);
      
      expect(result).toEqual(mockResponse);
      expect(globalThis.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/v1/query'),
        expect.objectContaining({
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(mockRequest),
        })
      );
    });

    it('should throw error on failed query', async () => {
      const mockRequest = {
        question: 'What is AI?',
      };
      
      (globalThis.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
        ok: false,
        json: async () => ({ detail: 'Query processing failed' }),
      });

      await expect(apiService.query(mockRequest)).rejects.toThrow('Query processing failed');
    });

    it('should handle query with all options', async () => {
      const mockRequest = {
        question: 'Test question',
        k: 5,
        return_sources: true,
        use_multi_agent: true,
        validate_answer: true,
        use_enterprise_api: true,
      };
      const mockResponse = {
        answer: 'Test answer',
        question: 'Test question',
        success: true,
        source_documents: [],
        validation: {
          relevance: 0.9,
          accuracy: 0.85,
          completeness: 0.8,
          clarity: 0.95,
          overall: 0.875,
          feedback: 'Good answer',
          passed: true,
        },
      };
      
      (globalThis.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const result = await apiService.query(mockRequest);
      
      expect(result).toEqual(mockResponse);
    });
  });
});
