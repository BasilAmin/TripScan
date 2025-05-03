import { useNavigate, useLocation } from "react-router-dom";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ArrowLeft, Calendar, MapPin, Clock, ListCheck, Users } from "lucide-react";
import { Separator } from "@/components/ui/separator";

const Itinerary = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { city } = location.state || { city: "Barcelona" }; // Default to Barcelona if no city is provided

  // Sample itinerary data - in a real app, this would be generated based on the selected city
  const itineraryData = {
    city,
    days: [
      {
        day: "Day 1",
        activities: [
          { time: "09:00 AM", activity: "Arrival and Hotel Check-in", description: "Get settled in and freshen up" },
          { time: "12:00 PM", activity: "Lunch at local restaurant", description: "Taste authentic local cuisine" },
          { time: "02:00 PM", activity: "Guided city tour", description: "Explore the main attractions" },
          { time: "07:00 PM", activity: "Dinner at waterfront", description: "Enjoy the sunset views" }
        ]
      },
      {
        day: "Day 2",
        activities: [
          { time: "08:00 AM", activity: "Breakfast at hotel", description: "Start your day with energy" },
          { time: "10:00 AM", activity: "Visit main museum", description: "Explore local art and history" },
          { time: "01:00 PM", activity: "Lunch in historic center", description: "Try traditional dishes" },
          { time: "03:00 PM", activity: "Shopping time", description: "Visit local artisans and markets" },
          { time: "08:00 PM", activity: "Dinner & cultural show", description: "Experience local entertainment" }
        ]
      },
      {
        day: "Day 3",
        activities: [
          { time: "09:00 AM", activity: "Day trip to nearby attraction", description: "Explore natural wonders" },
          { time: "12:30 PM", activity: "Picnic lunch", description: "Enjoy meal with a view" },
          { time: "04:00 PM", activity: "Return to hotel & relax", description: "Rest before evening activities" },
          { time: "07:00 PM", activity: "Farewell dinner", description: "Celebrate the journey at premium restaurant" }
        ]
      }
    ]
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <Button 
          variant="outline" 
          className="mb-6" 
          onClick={() => navigate(-1)}
        >
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to Results
        </Button>

        <Card className="border shadow-sm">
          <CardHeader className="py-6 border-b">
            <div className="flex flex-col md:flex-row md:justify-between md:items-center">
              <div>
                <CardTitle className="text-2xl flex items-center">
                  <MapPin className="mr-2 h-5 w-5 text-primary" />
                  {city} Itinerary
                </CardTitle>
                <CardDescription className="mt-1">
                  Your perfect 3-day travel plan
                </CardDescription>
              </div>
              
              <div className="mt-4 md:mt-0">
                <div className="flex items-center gap-2 text-sm text-muted-foreground">
                  <Calendar className="h-4 w-4" />
                  <span>3 Days</span>
                  <Separator orientation="vertical" className="h-4" />
                  <Users className="h-4 w-4" />
                  <span>Group Trip</span>
                </div>
              </div>
            </div>
          </CardHeader>
          
          <CardContent className="p-6">
            <div className="space-y-8">
              {itineraryData.days.map((day, dayIndex) => (
                <div key={dayIndex} className="pb-6 last:pb-0">
                  <h3 className="text-xl font-semibold mb-4 flex items-center">
                    <Calendar className="mr-2 h-5 w-5 text-primary" />
                    {day.day}
                  </h3>
                  
                  <div className="space-y-4">
                    {day.activities.map((activity, actIndex) => (
                      <Card key={actIndex} className="overflow-hidden">
                        <div className="p-4">
                          <div className="flex items-start">
                            <div className="bg-primary/10 p-2 rounded-full mr-3">
                              <Clock className="h-5 w-5 text-primary" />
                            </div>
                            <div>
                              <div className="font-medium">{activity.time}</div>
                              <div className="text-lg font-semibold mt-1">{activity.activity}</div>
                              <div className="text-muted-foreground text-sm mt-1">
                                {activity.description}
                              </div>
                            </div>
                          </div>
                        </div>
                      </Card>
                    ))}
                  </div>
                </div>
              ))}
            </div>
            
            <div className="mt-8 pt-6 border-t">
              <h3 className="text-xl font-semibold mb-4 flex items-center">
                <ListCheck className="mr-2 h-5 w-5 text-primary" />
                Travel Checklist
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                <Card className="p-3 bg-secondary/30">
                  <div className="flex items-center">
                    <div className="h-5 w-5 rounded-full bg-green-500 flex items-center justify-center mr-3">
                      <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <polyline points="20 6 9 17 4 12"></polyline>
                      </svg>
                    </div>
                    <span>Book flights</span>
                  </div>
                </Card>
                <Card className="p-3 bg-secondary/30">
                  <div className="flex items-center">
                    <div className="h-5 w-5 rounded-full bg-green-500 flex items-center justify-center mr-3">
                      <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <polyline points="20 6 9 17 4 12"></polyline>
                      </svg>
                    </div>
                    <span>Reserve hotel</span>
                  </div>
                </Card>
                <Card className="p-3 bg-secondary/30">
                  <div className="flex items-center">
                    <div className="h-5 w-5 rounded-full border border-gray-300 mr-3"></div>
                    <span>Check travel insurance</span>
                  </div>
                </Card>
                <Card className="p-3 bg-secondary/30">
                  <div className="flex items-center">
                    <div className="h-5 w-5 rounded-full border border-gray-300 mr-3"></div>
                    <span>Pack essentials</span>
                  </div>
                </Card>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Itinerary;