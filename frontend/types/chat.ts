export interface Message {
  id: number;
  conversation_id: number;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  metadata?: Record<string, any>;
}

export interface Conversation {
  id: number;
  user_id: string;
  title: string;
  created_at: string;
  updated_at: string;
}

export interface SendMessageRequest {
  message: string;
  conversation_id?: number;
}

export interface SendMessageResponse {
  message: string;
  conversation_id: number;
  timestamp: string;
}