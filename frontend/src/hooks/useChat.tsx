
import { useState, useEffect } from 'react';
import { MessageProps } from '@/components/Message';

// Mock users for the chat
const mockUsers = [
  {
    id: 'current-user',
    name: 'You',
    avatar: ''
  },
  {
    id: 'user1',
    name: 'Alex',
    avatar: ''
  },
  {
    id: 'user2',
    name: 'Morgan',
    avatar: ''
  },
  {
    id: 'user3',
    name: 'Taylor',
    avatar: ''
  }
];

// Initial mock messages
const initialMessages: MessageProps[] = [
  {
    id: '1',
    user: mockUsers[1],
    content: "Hey everyone! I found some great flight deals to Barcelona for next month. Who's interested?",
    timestamp: new Date(Date.now() - 1000 * 60 * 60 * 2), // 2 hours ago
    isCurrentUser: false
  },
  {
    id: '2',
    user: mockUsers[2],
    content: "Barcelona sounds amazing! What dates are you looking at?",
    timestamp: new Date(Date.now() - 1000 * 60 * 55), // 55 minutes ago
    isCurrentUser: false
  },
  {
    id: '3',
    user: mockUsers[3],
    content: "I've been wanting to visit Sagrada Familia forever. Count me in if it's mid-month!",
    timestamp: new Date(Date.now() - 1000 * 60 * 40), // 40 minutes ago
    isCurrentUser: false
  }
];

export const useChat = () => {
  const [messages, setMessages] = useState<MessageProps[]>(initialMessages);
  const [isLoading, setIsLoading] = useState(false);
  
  const currentUser = mockUsers[0];
  
  const sendMessage = (content: string) => {
    if (!content.trim()) return;
    
    const newMessage: MessageProps = {
      id: Date.now().toString(),
      user: currentUser,
      content,
      timestamp: new Date(),
      isCurrentUser: true
    };
    
    setMessages(prev => [...prev, newMessage]);
    
    // Simulate a response after a short delay
    setIsLoading(true);
    setTimeout(() => {
      const responseUser = mockUsers[Math.floor(Math.random() * (mockUsers.length - 1)) + 1];
      
      const responses = [
        "That sounds great! Let me check my calendar.",
        "I might be able to join. What's the budget looking like?",
        "I've been to Barcelona before, the beaches are amazing!",
        "Should we book accommodations together too?",
        "Has anyone found good restaurants we should try there?"
      ];
      
      const responseMessage: MessageProps = {
        id: (Date.now() + 1).toString(),
        user: responseUser,
        content: responses[Math.floor(Math.random() * responses.length)],
        timestamp: new Date(),
        isCurrentUser: false
      };
      
      setMessages(prev => [...prev, responseMessage]);
      setIsLoading(false);
    }, 1500);
  };
  
  return {
    messages,
    sendMessage,
    currentUser,
    isLoading
  };
};
