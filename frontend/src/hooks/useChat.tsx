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
      console.log('Fetching messages...');
      console.log(api.defaults.baseURL);  // Log the base URL to ensure it's correct
      const response = await api.get(`/getMessages/`);  // Ensure that this matches the FastAPI endpoint
      console.log('Fetched data:', response.data);
      const fetchedMessages = response.data.map((msg: any) => ({
        id: msg.message_id,  // You should ensure the response includes message_id
        user: { 
          id: msg.user_id, 
          name: msg.user_id === userId ? 'You' : 'Other', 
          avatar: '' 
        },
        content: msg.content,
        timestamp: new Date(msg.timestamp),  // Ensure the response includes a timestamp
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
      await api.post(`/sendMessage/`, {
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

  // Fetch messages on component mount and set up polling for new messages
  useEffect(() => {
    fetchMessages(); // Initial fetch
    const interval = setInterval(() => {
      fetchMessages(); // Fetch new messages every 2 seconds
    }, 2000);

    // Clean up the interval on unmount
    return () => clearInterval(interval);
  }, [userId]);


  return {
    messages,
    sendMessage,
    currentUser,
    isLoading,
  };
};
