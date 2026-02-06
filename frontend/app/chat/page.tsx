'use client';

import React, { useState } from 'react';
import { useAuth } from '../../hooks/useAuth';
import { useChat } from '../../hooks/useChat';
import ChatWindow from '../../components/chat/ChatWindow';
import ConversationHistory from '../../components/chat/ConversationHistory';
import ProtectedRoute from '../../components/auth/ProtectedRoute';

const ChatPage = () => {
  const { user } = useAuth();
  const [sidebarOpen, setSidebarOpen] = useState(true);

  // Use the chat hook with the current user
  const {
    messages,
    conversations,
    isLoading,
    error,
    currentConversationId,
    sendMessage,
    fetchConversationMessages,
    createNewConversation,
    fetchConversations,
  } = useChat(user?.id || '');

  // Toggle sidebar on mobile
  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  return (
    <ProtectedRoute>
      <div className="flex h-screen bg-gray-100">
        {/* Sidebar for conversation history */}
        <div className={`${sidebarOpen ? 'block' : 'hidden'} md:block`}>
          <ConversationHistory
            conversations={conversations}
            onSelectConversation={(id) => fetchConversationMessages(id)}
            onCreateNew={createNewConversation}
            currentConversationId={currentConversationId}
          />
        </div>

        {/* Main chat area */}
        <div className="flex-1 flex flex-col">
          {/* Mobile header */}
          <div className="md:hidden p-4 bg-white border-b border-gray-300 flex items-center justify-between">
            <div className="flex items-center">
              <button
                onClick={toggleSidebar}
                className="mr-4 text-gray-600"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              </button>
              <h1 className="text-xl font-semibold">Chat</h1>
            </div>
            <a
              href="/tasks"
              className="text-sm bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700"
            >
              Tasks
            </a>
          </div>

          {/* Chat window */}
          <div className="flex-1 overflow-hidden">
            <ChatWindow
              messages={messages}
              onSendMessage={sendMessage}
              isLoading={isLoading}
              title={currentConversationId ? 'Chat' : 'New Conversation'}
            />
          </div>
        </div>

        {/* Error message */}
        {error && (
          <div className="fixed bottom-4 right-4 bg-red-500 text-white p-4 rounded-lg shadow-lg">
            {error}
            <button
              onClick={() => fetchConversations()} // Retry
              className="ml-4 underline"
            >
              Retry
            </button>
          </div>
        )}
      </div>
    </ProtectedRoute>
  );
};

export default ChatPage;