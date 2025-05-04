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
      const response = await api.get(`/getMessages/`);  // Ensure that this matches the FastAPI endpoint
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
        if (!content.trim()) {
          content = "Image upload";
      }
        // Send the image message
        const base64Image = await convertImageToBase64(image);
        const userData = {
          user_id: userId,
          content: content,
          image: base64Image,
        };
        console.log('Sending image data:', userData); // Log the data being sent
        // Call the /sendMessageImage endpoint to send the image
        await api.post(
          "/sendMessageImage/", 
          userData,  // Pass userData directly as the body
          {
            headers: {
              "Content-Type": "application/json", // Ensure it's set to application/json
            }
          }
        );
        
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

  // Helper function to convert image to base64
  const convertImageToBase64 = (image: File): Promise<string> => {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onloadend = () => resolve(reader.result as string);
        reader.onerror = reject;
        reader.readAsDataURL(image);
    });
  };

  // Poll messages every 2 seconds
  useEffect(() => {
    fetchMessages(); // initial load

    const interval = setInterval(fetchMessages, 2000); // poll every 2s

    return () => clearInterval(interval); // cleanup on unmount
  }, []);

  return {
    messages,
    sendMessage,
    currentUser,
    isLoading,
    clearMessages,
  };
};
