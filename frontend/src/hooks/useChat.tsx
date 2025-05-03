import { useState, useEffect } from 'react';
import { MessageProps } from '@/components/Message';
import api from '@/lib/axios';

export const useChat = (userId: string) => {
  const [messages, setMessages] = useState<MessageProps[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const currentUser = { id: userId, name: 'You', avatar: '' };

  // Fetch messages from the server
  const fetchMessages = async () => {
    try {
      const response = await api.get(`/getMessages`);
      const fetchedMessages = response.data.map((msg: any) => ({
        id: msg.message_id,
        user: { id: msg.user_id, name: msg.user_id === userId ? 'You' : 'Other', avatar: '' },
        content: msg.content,
        timestamp: new Date(msg.timestamp),
        isCurrentUser: msg.user_id === userId,
      }));
      setMessages(fetchedMessages);
    } catch (error) {
      console.error('Error fetching messages:', error);
    }
  };

  // Send a new message
  const sendMessage = async (content: string) => {
    if (!content.trim()) return;

    const newMessage: MessageProps = {
      id: Date.now().toString(),
      user: currentUser,
      content,
      timestamp: new Date(),
      isCurrentUser: true,
    };

    setMessages((prev) => [...prev, newMessage]);

    try {
      setIsLoading(true);
      await api.post(`/sendMessage`, {
        user_id: userId,
        content,
      });
      await fetchMessages(); // Refresh messages after sending
    } catch (error) {
      console.error('Error sending message:', error);
    } finally {
      setIsLoading(false);
    }
  };

  // Fetch messages on component mount
  useEffect(() => {
    fetchMessages();
  }, []);

  return {
    messages,
    sendMessage,
    currentUser,
    isLoading,
  };
};