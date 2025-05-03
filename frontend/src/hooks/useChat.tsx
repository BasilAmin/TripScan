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
  const sendMessage = async (content: string, image?: File) => {
    if (!content.trim() && !image) return; // Don't send empty messages
  
    const newMessage: MessageProps = {
      id: Date.now().toString(),
      user: currentUser,
      image: image ? URL.createObjectURL(image) : undefined,
      content: content, // Attach text content if provided
      timestamp: new Date(),
      isCurrentUser: true,
    };
  
    setMessages((prev) => [...prev, newMessage]);
  
    try {
      setIsLoading(true);
  
      if (image) {
        // Send the image message
        const formData = new FormData();
        formData.append("user_id", userId);
        formData.append("image", image);
        formData.append("content", content); // Attach content even if it’s empty (for context)
  
        // Call the /sendMessageImage endpoint to send the image
        await api.post(`/sendMessageImage/`, formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        });
      } else {
        // Send the text message
        await api.post(`/sendMessage/`, {
          user_id: userId,
          content: content,
        });
      }
  
      // Fetch updated messages
      await fetchMessages();
    } catch (error) {
      console.error('Error sending message:', error);
    } finally {
      setIsLoading(false);
    }
  };

  // Add clearMessages function to reset chat to empty
  const clearMessages = async () => {
    try {
      await api.get('/clear_chat');
      setMessages([]);
    } catch (error) {
      console.error('Error clearing messages:', error);
    }
  };

  return {
    messages,
    sendMessage,
    currentUser,
    isLoading,
    clearMessages,
  };
};
