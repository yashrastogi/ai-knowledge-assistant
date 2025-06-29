import { useState } from 'react';
import { Send, Bot, User, CheckCircle, XCircle, AlertTriangle } from 'lucide-react';
import { apiService, QueryResponse } from '../services/api';
import './ChatInterface.css';

interface Message {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  response?: QueryResponse;
  timestamp: Date;
}

export function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [useMultiAgent, setUseMultiAgent] = useState(true);
  const [validateAnswer, setValidateAnswer] = useState(true);
  const [useEnterpriseAPI, setUseEnterpriseAPI] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: input,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await apiService.query({
        question: input,
        k: 4,
        return_sources: true,
        use_multi_agent: useMultiAgent,
        validate_answer: validateAnswer,
        use_enterprise_api: useEnterpriseAPI,
      });

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: response.answer,
        response,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: `Error: ${error instanceof Error ? error.message : 'Unknown error occurred'}`,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <div className="header-content">
          <Bot size={24} />
          <h1>AI Knowledge Assistant</h1>
        </div>
        <div className="header-options">
          <label>
            <input
              type="checkbox"
              checked={useMultiAgent}
              onChange={(e) => setUseMultiAgent(e.target.checked)}
            />
            Multi-Agent
          </label>
          <label>
            <input
              type="checkbox"
              checked={validateAnswer}
              onChange={(e) => setValidateAnswer(e.target.checked)}
              disabled={!useMultiAgent}
            />
            Validate
          </label>
          <label>
            <input
              type="checkbox"
              checked={useEnterpriseAPI}
              onChange={(e) => setUseEnterpriseAPI(e.target.checked)}
            />
            Enterprise API
          </label>
        </div>
      </div>

      <div className="chat-messages">
        {messages.length === 0 && (
          <div className="empty-state">
            <Bot size={48} />
            <p>Ask me anything about the knowledge base!</p>
            <div className="example-questions">
              <button onClick={() => setInput('What is RAG?')}>What is RAG?</button>
              <button onClick={() => setInput('What incidents are currently open?')}>
                What incidents are open?
              </button>
              <button onClick={() => setInput('Tell me about our production servers')}>
                About production servers
              </button>
            </div>
          </div>
        )}

        {messages.map((message) => (
          <div key={message.id} className={`message ${message.type}`}>
            <div className="message-icon">
              {message.type === 'user' ? <User size={20} /> : <Bot size={20} />}
            </div>
            <div className="message-content">
              <div className="message-text">{message.content}</div>

              {message.response && (
                <div className="message-metadata">
                  {/* Agent Workflow */}
                  {message.response.agent_workflow && (
                    <div className="workflow">
                      <strong>Agents:</strong> {message.response.agent_workflow.join(' → ')}
                    </div>
                  )}

                  {/* Validation Scores */}
                  {message.response.validation && (
                    <div className="validation">
                      <div className="validation-header">
                        {message.response.validation.passed ? (
                          <CheckCircle size={16} className="icon-success" />
                        ) : (
                          <XCircle size={16} className="icon-error" />
                        )}
                        <strong>Validation Score: {message.response.validation.overall}/10</strong>
                      </div>
                      <div className="validation-scores">
                        <span>Relevance: {message.response.validation.relevance}</span>
                        <span>Accuracy: {message.response.validation.accuracy}</span>
                        <span>Completeness: {message.response.validation.completeness}</span>
                        <span>Clarity: {message.response.validation.clarity}</span>
                      </div>
                      {message.response.validation.feedback && (
                        <div className="validation-feedback">{message.response.validation.feedback}</div>
                      )}
                    </div>
                  )}

                  {/* Warning */}
                  {message.response.warning && (
                    <div className="warning">
                      <AlertTriangle size={16} />
                      {message.response.warning}
                    </div>
                  )}

                  {/* Source Documents */}
                  {message.response.source_documents && message.response.source_documents.length > 0 && (
                    <details className="sources">
                      <summary>
                        <strong>Sources ({message.response.source_documents.length})</strong>
                      </summary>
                      {message.response.source_documents.map((doc, idx) => (
                        <div key={idx} className="source-doc">
                          <div className="source-header">Source {idx + 1}</div>
                          <div className="source-preview">{doc.preview}</div>
                          {Object.keys(doc.metadata).length > 0 && (
                            <div className="source-metadata">
                              {Object.entries(doc.metadata).map(([key, value]) => (
                                <span key={key}>
                                  {key}: {String(value)}
                                </span>
                              ))}
                            </div>
                          )}
                        </div>
                      ))}
                    </details>
                  )}

                  {/* Enterprise Data */}
                  {message.response.enterprise_data && (
                    <details className="enterprise-data">
                      <summary>
                        <strong>Enterprise Data</strong>
                      </summary>
                      <pre>{message.response.enterprise_data}</pre>
                    </details>
                  )}
                </div>
              )}

              <div className="message-time">{message.timestamp.toLocaleTimeString()}</div>
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="message assistant loading">
            <div className="message-icon">
              <Bot size={20} />
            </div>
            <div className="message-content">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
      </div>

      <form className="chat-input" onSubmit={handleSubmit}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask a question..."
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading || !input.trim()}>
          <Send size={20} />
        </button>
      </form>
    </div>
  );
}
