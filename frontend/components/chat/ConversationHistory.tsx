import React from 'react';
import { Conversation } from '../../types/chat';

interface ConversationHistoryProps {
  conversations: Conversation[];
  onSelectConversation: (conversationId: number) => void;
  onCreateNew: () => void;
  currentConversationId: number | null;
}

const ConversationHistory: React.FC<ConversationHistoryProps> = ({
  conversations,
  onSelectConversation,
  onCreateNew,
  currentConversationId,
}) => {
  return (
    <div className="border-r border-gray-300 w-64 flex-shrink-0 bg-gray-50">
      <div className="p-4">
        <button
          onClick={onCreateNew}
          className="w-full bg-blue-500 text-white py-2 px-4 rounded-lg mb-4 hover:bg-blue-600 transition-colors"
        >
          New Chat
        </button>

        <h3 className="font-semibold mb-2">Previous Chats</h3>
        <div className="space-y-1">
          {conversations.map((conversation) => (
            <button
              key={conversation.id}
              onClick={() => onSelectConversation(conversation.id)}
              className={`w-full text-left p-2 rounded-lg text-sm truncate ${
                currentConversationId === conversation.id
                  ? 'bg-blue-100 text-blue-800'
                  : 'hover:bg-gray-200'
              }`}
            >
              <div className="font-medium truncate">{conversation.title}</div>
              <div className="text-xs text-gray-500">
                {new Date(conversation.updated_at).toLocaleDateString()}
              </div>
            </button>
          ))}
        </div>
        {conversations.length === 0 && (
          <p className="text-gray-500 text-sm">No conversations yet</p>
        )}
      </div>
    </div>
  );
};

export default ConversationHistory;