import { useState, KeyboardEvent, useRef } from 'react';
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { MessageCircle, Image } from "lucide-react";
import { toast } from "@/components/ui/sonner";

interface MessageInputProps {
  onSendMessage: (content: string, image?: File) => void;
  disabled?: boolean;
}

const MessageInput = ({ onSendMessage, disabled = false }: MessageInputProps) => {
  const [message, setMessage] = useState('');
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const imageInputRef = useRef<HTMLInputElement>(null);

  const handleSendMessage = () => {
      if ((message.trim() || selectedImage) && !disabled) {
        onSendMessage(message, selectedImage || undefined);
      setMessage('');
      setSelectedImage(null);
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleImageSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      // Check file type
      if (!file.type.startsWith('image/')) {
        toast.error("Please select an image file");
        return;
      }
      
      // Check file size (5MB max)
      if (file.size > 5 * 1024 * 1024) {
        toast.error("Image size should be less than 5MB");
        return;
      }
      
      setSelectedImage(file);
      toast.success(`Selected image: ${file.name}`);
    }
  };

  const triggerImageUpload = () => {
    imageInputRef.current?.click();
  };

  return (
    <div className="flex flex-col p-4 border-t">
      {selectedImage && (
        <div className="mb-2 p-2 bg-secondary/50 rounded flex items-center justify-between">
          <div className="flex items-center">
            <div className="w-8 h-8 bg-secondary rounded flex items-center justify-center mr-2">
              <Image className="w-4 h-4" />
            </div>
            <span className="text-sm truncate max-w-[150px]">{selectedImage.name}</span>
          </div>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setSelectedImage(null)}
            className="h-6 w-6"
          >
            ×
          </Button>
        </div>
      )}
      
      <div className="flex items-end gap-2">
        <input
          type="file"
          accept="image/*"
          ref={imageInputRef}
          onChange={handleImageSelect}
          className="hidden"
        />
        
        <Button
          type="button"
          size="icon"
          variant="outline"
          onClick={triggerImageUpload}
          disabled={disabled}
          className="h-[60px] w-[60px] rounded-full"
        >
          <Image className="h-5 w-5" />
        </Button>
        
        <Textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type a message..."
          disabled={disabled}
          className="min-h-[60px] resize-none"
        />
        
        <Button 
          onClick={handleSendMessage} 
          disabled={(!message.trim() && !selectedImage) || disabled}
          size="icon"
          className="h-[60px] w-[60px] rounded-full"
        >
          <MessageCircle className="h-5 w-5" />
        </Button>
      </div>
    </div>
  );
};

export default MessageInput;
