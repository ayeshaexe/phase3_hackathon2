import { useState, useEffect } from 'react';
import { apiClient } from '../lib/api-client';
import { Message, Conversation } from '../types/chat';

export const useChat = (userId: string) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [currentConversationId, setCurrentConversationId] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Fetch conversations for the user
  const fetchConversations = async () => {
    try {
      setIsLoading(true);
      const response = await apiClient.getUserConversations(userId);

      if (response.data) {
        setConversations(response.data.conversations || []);
      }
    } catch (err) {
      setError('Failed to fetch conversations');
      console.error('Error fetching conversations:', err);
    } finally {
      setIsLoading(false);
    }
  };

  // Fetch messages for a specific conversation
  const fetchConversationMessages = async (conversationId: number) => {
    try {
      setIsLoading(true);
      setCurrentConversationId(conversationId);

      const response = await apiClient.getConversation(userId, conversationId);

      if (response.data) {
        setMessages(response.data.messages || []);
      }
    } catch (err) {
      setError('Failed to fetch conversation messages');
      console.error('Error fetching conversation messages:', err);
    } finally {
      setIsLoading(false);
    }
  };

  // Send a message
  const sendMessage = async (message: string) => {
    if (!message.trim()) return;

    try {
      setIsLoading(true);
      setError(null);

      // Add user message optimistically
      const userMessage: Message = {
        id: Date.now(), // Temporary ID
        conversation_id: currentConversationId || 0,
        role: 'user',
        content: message,
        timestamp: new Date().toISOString(),
      };

      setMessages(prev => [...prev, userMessage]);

      // Send message to API
      const response = await apiClient.sendMessage(userId, message, currentConversationId);

      if (response.data) {
        const aiMessage: Message = {
          id: Date.now() + 1, // Temporary ID
          conversation_id: response.data.conversation_id,
          role: 'assistant',
          content: response.data.message,
          timestamp: response.data.timestamp,
        };

        // Update messages with AI response
        setMessages(prev => {
          const updated = [...prev];
          // Replace the temporary user message if needed and add AI response
          return [...updated.slice(0, -1), userMessage, aiMessage];
        });

        // Update conversation ID if it's a new conversation
        if (!currentConversationId && response.data.conversation_id) {
          setCurrentConversationId(response.data.conversation_id);
          await fetchConversations(); // Refresh conversations list
        }
      }
    } catch (err) {
      setError('Failed to send message');
      console.error('Error sending message:', err);

      // Remove the optimistic user message if failed
      setMessages(prev => prev.slice(0, -1));
    } finally {
      setIsLoading(false);
    }
  };

  // Create new conversation
  const createNewConversation = () => {
    setMessages([]);
    setCurrentConversationId(null);
  };

  // Load conversations on userId change
  useEffect(() => {
    if (userId) {
      fetchConversations();
    }
  }, [userId]);

  return {
    messages,
    conversations,
    isLoading,
    error,
    currentConversationId,
    sendMessage,
    fetchConversationMessages,
    createNewConversation,
    fetchConversations,
  };
};