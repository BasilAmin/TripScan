import { useState, useEffect } from 'react';

export interface DestinationScore {
  city: string;
  score: number;
}

// This would normally be fetched from an API
const mockLlmResponse = `
Barcelona,0.92
Paris,0.87
Tokyo,0.78
New York,0.76
Rome,0.71
`;

export const useLlmResults = () => {
  const [destinationScores, setDestinationScores] = useState<DestinationScore[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);
  
  useEffect(() => {
    const fetchLlmResults = async () => {
      try {
        // Simulate API call with a delay
        await new Promise(resolve => setTimeout(resolve, 1500));
        
        // In a real app, this would be a fetch to your LLM API
        // const response = await fetch('/api/analyze-chat');
        // const data = await response.text();
        
        // Parse CSV format (destination,score)
        const parsedScores = mockLlmResponse
          .trim()
          .split('\n')
          .map(line => {
            const [city, scoreStr] = line.split(',');
            return {
              city: city.trim(),
              score: parseFloat(scoreStr.trim())
            };
          });
        
        setDestinationScores(parsedScores);
        setIsLoading(false);
      } catch (err) {
        console.error('Error fetching LLM results:', err);
        setError(err instanceof Error ? err : new Error('Unknown error'));
        setIsLoading(false);
      }
    };
    
    fetchLlmResults();
  }, []);
  
  return {
    destinationScores,
    isLoading,
    error
  };
};