
import { useChat } from '@/hooks/useChat';
import MessageList from './MessageList';
import MessageInput from './MessageInput';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Users } from "lucide-react";
import { getOrCreateUserId} from "@/lib/utils";

const user_id = getOrCreateUserId();

const GroupChat = () => {
  const { messages, sendMessage, currentUser, isLoading } = useChat(user_id);

  return (
    <Card className="mt-8 border shadow-sm">
      <CardHeader className="py-4 border-b">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Users className="h-5 w-5 text-primary" />
            <div>
              <CardTitle className="text-lg">Travel Group Chat</CardTitle>
              <CardDescription className="text-xs">
                {messages.length > 0 ? `${messages.length} messages` : 'No messages yet'}
              </CardDescription>
            </div>
          </div>
        </div>
      </CardHeader>
      <CardContent className="p-0 flex flex-col h-[500px]">
        <div className="flex-1 overflow-hidden">
          <MessageList messages={messages} currentUserId={currentUser.id} />
        </div>
        <MessageInput onSendMessage={sendMessage} disabled={isLoading} />
      </CardContent>
    </Card>
  );
};

export default GroupChat;
