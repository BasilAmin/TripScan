import { useState, useEffect } from 'react';
import api from '@/lib/axios'; 

export interface DestinationScore {
  city: string;
  country: string;
  score: number;
  features: Record<string, number>;
  imageUrl: string;
}

export interface AggregatePreferences {
  [key: string]: number;
}

export const useLlmResults = () => {
    const [destinationScores, setDestinationScores] = useState<DestinationScore[]>([]);
    const [aggregatePreferences, setAggregatePreferences] = useState<AggregatePreferences>({});
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<Error | null>(null);
  
    const fetchLlmResults = async () => {
      try {
        setIsLoading(true);
        const response = await api.get('/recommendations');
        const data = response.data;
  
        if (!data.top_recommendations) {
          throw new Error('Invalid response structure');
        }
  
        const resultsWithImages = await Promise.all(
          data.top_recommendations.map(async (item: any) => {
            try {
            
              const res = await api.get(`/city-image/${encodeURIComponent(item.city)}`);
              console.log(`Image URL:`, res.data.image_url);
              const imageUrl = res.data.image_url;
  
              return {
                ...item,
                score: Math.round(item.match_score),
                imageUrl,
              };
            } catch (error) {
              console.error(`Failed to fetch image for ${item.city}`, error);
              return {
                ...item,
                score: Math.round(item.match_score),
                imageUrl: '', // Default or fallback image URL
              };
            }
          })
        );
  
        setDestinationScores(resultsWithImages);
        setAggregatePreferences(data.aggregate_preferences || {});
      } catch (err) {
        console.error('Error fetching LLM results:', err);
        setError(err instanceof Error ? err : new Error('Unknown error'));
      } finally {
        setIsLoading(false);
      }
    };
  
    useEffect(() => {
      fetchLlmResults();
    }, []);
  
    return {
      destinationScores,
      aggregatePreferences,
      isLoading,
      error,
    };
};
