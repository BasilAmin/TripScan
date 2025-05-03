
import { useRef, useEffect } from 'react';
import Message, { MessageProps } from './Message';
import { ScrollArea } from "@/components/ui/scroll-area";

interface MessageListProps {
  messages: MessageProps[];
  currentUserId: string;
}

const MessageList = ({ messages, currentUserId }: MessageListProps) => {
  const scrollRef = useRef<HTMLDivElement>(null);
  
  // Scroll to bottom on new messages
  useEffect(() => {
    if (scrollRef.current) {
      const scrollContainer = scrollRef.current;
      scrollContainer.scrollTop = scrollContainer.scrollHeight;
    }
  }, [messages]);

  if (messages.length === 0) {
    return (
      <div className="h-full flex items-center justify-center text-center p-4">
        <div className="text-muted-foreground">
          <p className="mb-2">No messages yet</p>
          <p className="text-sm">Start the conversation by sending a message below!</p>
        </div>
      </div>
    );
  }

  return (
    <ScrollArea 
      ref={scrollRef} 
      className="h-full px-4"
    >
      <div className="py-4">
        {messages.map((message) => (
          <Message
            key={message.id}
            {...message}
            isCurrentUser={message.user.id === currentUserId}
          />
        ))}
      </div>
    </ScrollArea>
  );
};

export default MessageList;
