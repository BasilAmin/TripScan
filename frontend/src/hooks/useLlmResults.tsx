import { useState, useEffect } from 'react';
import api from '@/lib/axios'; 

export interface DestinationScore {
  city: string;
  country: string;
  score: number;
  features: Record<string, number>;
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
      const response = await api.get('/recommendations'); // Replace with your FastAPI endpoint
      const data = response.data;

      if (!data.top_recommendations) {
        throw new Error('Invalid response structure');
      }

      const updatedScores = data.top_recommendations.map((item: any) => ({
        ...item,
        score: Math.round(item.match_score),
      }));

      setDestinationScores(updatedScores);
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
