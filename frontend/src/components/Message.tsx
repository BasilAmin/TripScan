
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { cn } from "@/lib/utils";

export interface MessageProps {
  id: string;
  user: {
    id: string;
    name: string;
    avatar?: string;
  };
  content: string;
  timestamp: Date;
  isCurrentUser: boolean;
}

const Message = ({ user, content, timestamp, isCurrentUser }: MessageProps) => {
  const formattedTime = new Intl.DateTimeFormat('en-US', {
    hour: 'numeric',
    minute: 'numeric',
    hour12: true,
  }).format(timestamp);

  return (
    <div className={cn(
      "flex gap-3 mb-4",
      isCurrentUser ? "flex-row-reverse" : "flex-row"
    )}>
      <Avatar className="h-8 w-8">
        <AvatarImage src={user.avatar} alt={user.name} />
        <AvatarFallback>{user.name.substring(0, 2).toUpperCase()}</AvatarFallback>
      </Avatar>
      
      <div className={cn(
        "flex flex-col",
        isCurrentUser ? "items-end" : "items-start"
      )}>
        <div className="flex items-center gap-2">
          {!isCurrentUser && (
            <span className="text-sm font-medium">{user.name}</span>
          )}
          <span className="text-xs text-muted-foreground message-time">{formattedTime}</span>
        </div>
        
        <div className={cn(
          "message-bubble rounded-lg px-4 py-2 mt-1",
          isCurrentUser ? 
            "bg-primary text-white rounded-tr-none" : 
            "bg-secondary text-foreground rounded-tl-none"
        )}>
          {content}
        </div>
      </div>
    </div>
  );
};

export default Message;
