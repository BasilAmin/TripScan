
import { useChat } from '@/hooks/useChat';
import MessageList from './MessageList';
import MessageInput from './MessageInput';
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from "@/components/ui/card";
import { getOrCreateUserId} from "@/lib/utils";
import { Brain, Calendar, Trash2, Users } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";
import { toast } from "@/components/ui/sonner";

const user_id = getOrCreateUserId();

const GroupChat = () => {
  const { messages, sendMessage, currentUser, isLoading, clearMessages} = useChat(user_id);
  const navigate = useNavigate();

  const handleThinkingRequest = () => {
    sendMessage("Can we get some recommendations?");
  };

  const handleNegotiateDates = () => {
    sendMessage("Can we discuss possible travel dates that work for everyone?");
  };

  const handleClearConversation = () => {
    clearMessages();
    toast.success("Conversation cleared");
  };

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
          <div className="flex space-x-2">
          <Button 
              variant="outline" 
              size="sm" 
              className="flex items-center gap-1 text-red-500 hover:bg-red-50 hover:text-red-600"
              onClick={handleClearConversation}
            >
              <Trash2 className="h-4 w-4" />
              <span className="hidden sm:inline">Clear</span>
            </Button>
            <Button 
              variant="outline" 
              size="sm" 
              className="flex items-center gap-1"
              onClick={handleThinkingRequest}
            >
              <Brain className="h-4 w-4" />
              <span className="hidden sm:inline">Think</span>
            </Button>
            <Button 
              variant="outline" 
              size="sm" 
              className="flex items-center gap-1"
              onClick={handleNegotiateDates}
            >
              <Calendar className="h-4 w-4" />
              <span className="hidden sm:inline">Negotiate Dates</span>
            </Button>
          </div>
        </div>
      </CardHeader>
      <CardContent className="p-0 flex flex-col h-[500px]">
        <div className="flex-1 overflow-hidden">
          <MessageList messages={messages} currentUserId={currentUser.id} />
        </div>
        <MessageInput onSendMessage={sendMessage} disabled={isLoading} />
      </CardContent>
      <CardFooter className="border-t p-4 bg-gray-50">
        <div className="w-full flex justify-center">
          <Button 
            onClick={() => navigate('/results')}
            className="bg-primary hover:bg-primary/90"
          >
            See Travel Recommendations
          </Button>
        </div>
      </CardFooter>
    </Card>
  );
};

export default GroupChat;
