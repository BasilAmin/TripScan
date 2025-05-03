import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { ArrowLeft, Trophy } from "lucide-react";
import { useLlmResults } from "@/hooks/useLlmResults";

const Results = () => {
  const navigate = useNavigate();
  const { destinationScores, isLoading, error } = useLlmResults();
  const [cityImages, setCityImages] = useState({});

  // Sort destinations by score and take top 3
  const topDestinations = [...destinationScores]
    .sort((a, b) => b.score - a.score)
    .slice(0, 3);

  // Fetch images for each city
  useEffect(() => {
    const fetchImages = async () => {
      const images = {};
      for (const destination of topDestinations) {
        try {
          const response = await fetch(`/city-image/${destination.city}`);
          if (response.ok) {
            const data = await response.json();
            images[destination.city] = data.image_url;
          }
        } catch (err) {
          console.error(`Failed to fetch image for ${destination.city}:`, err);
          images[destination.city] = 'https://via.placeholder.com/400x300?text=Image+Not+Found';
        }
      }
      setCityImages(images);
    };

    if (topDestinations.length > 0) {
      fetchImages();
    }
  }, [topDestinations]);

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <Button 
          variant="outline" 
          className="mb-6" 
          onClick={() => navigate('/')}
        >
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to Chat
        </Button>

        <Card className="border shadow-sm">
          <CardHeader className="py-4 border-b">
            <div className="flex items-center justify-between">
              <div>
                <CardTitle className="text-2xl">Travel Recommendations</CardTitle>
                <CardDescription>
                  Based on your group conversation, here are the top destinations
                </CardDescription>
              </div>
            </div>
          </CardHeader>
          <CardContent className="p-6">
            {isLoading ? (
              <div className="flex justify-center items-center h-64">
                <div className="animate-pulse text-center">
                  <p className="text-lg font-medium text-gray-500">Analyzing your conversation...</p>
                  <p className="text-sm text-gray-400">Finding the best destinations for your group</p>
                </div>
              </div>
            ) : error ? (
              <div className="text-center text-red-500 p-4">
                <p>Failed to analyze your conversation. Please try again later.</p>
              </div>
            ) : (
              <>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                  {topDestinations.map((destination, index) => (
                    <Card key={destination.city} className="overflow-hidden">
                      <div className={`h-2 ${index === 0 ? 'bg-yellow-400' : index === 1 ? 'bg-gray-300' : 'bg-amber-600'}`}></div>
                      <CardContent className="p-4 text-center">
                        <div className="flex justify-center mb-2">
                          <Trophy className={`h-8 w-8 ${index === 0 ? 'text-yellow-400' : index === 1 ? 'text-gray-300' : 'text-amber-600'}`} />
                        </div>
                        <h3 className="text-xl font-bold">{destination.city}</h3>
                        <div className="mt-2">
                          <span className="text-3xl font-bold">
                            {Math.round(destination.score)}
                          </span>
                          <span className="text-gray-500 text-sm ml-1">/ 100</span>
                        </div>
                        <img
                          src={cityImages[destination.city] || `https://i.natgeofe.com/k/5b396b5e-59e7-43a6-9448-708125549aa1/new-york-statue-of-liberty_16x9.jpg?w=1200`}
                          alt={destination.city}
                          className="mt-4 rounded-lg shadow-md object-cover w-full h-48"
                          onError={(e) => {
                            e.target.src = 'https://via.placeholder.com/400x300?text=Image+Not+Found';
                          }}
                        />
                      </CardContent>
                    </Card>
                  ))}
                </div>

                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Rank</TableHead>
                      <TableHead>Destination</TableHead>
                      <TableHead>Score</TableHead>
                      <TableHead>Compatibility</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {topDestinations.map((destination, index) => (
                      <TableRow key={destination.city}>
                        <TableCell className="font-medium">#{index + 1}</TableCell>
                        <TableCell>{destination.city}</TableCell>
                        <TableCell>{Math.round(destination.score)}/100</TableCell>
                        <TableCell>
                          <div className="w-full bg-gray-200 rounded-full h-2.5">
                            <div
                              className={`h-2.5 rounded-full ${
                                index === 0 ? 'bg-primary' : index === 1 ? 'bg-blue-400' : 'bg-blue-300'
                              }`}
                              style={{ width: `${destination.score}%` }}
                            ></div>
                          </div>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Results;