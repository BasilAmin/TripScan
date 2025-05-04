import { useEffect, useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ArrowLeft, Calendar, MapPin, Clock, ListCheck, Users, Plane, Hotel } from "lucide-react";
import { Separator } from "@/components/ui/separator";
import api from "@/lib/axios";
import { getOrCreateUserId } from "@/lib/utils";

interface HotelInfo {
  name: string;
  price: number;
}

interface FlightInfo {
  departure_time: {
    year: number;
    month: number;
    day: number;
    hour: number;
    minute: number;
    second: number;
  };
  origin: string;
  destination: string;
  airline: string;
  price: number;
}

const user_id = getOrCreateUserId();

const Itinerary = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { city } = location.state || { city: "Barcelona" };

  const [hotel, setHotel] = useState<HotelInfo | null>(null);
  const [flights, setFlights] = useState<{ go: FlightInfo | null; return: FlightInfo | null }>({
    go: null,
    return: null,
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchItineraryData = async () => {
      try {
        const [hotelRes, flightRes] = await Promise.all([
          api.get(`/hotels/`, { params: { city } }),
          api.get(`/flight_info`, { params: { city: city, user_id: user_id } }),
        ]);

        setHotel(hotelRes.data); // Assuming the response contains name and price
        setFlights({
          go: flightRes.data.outbound,
          return: flightRes.data.inbound,
        });
      } catch (error) {
        console.error("Error fetching itinerary data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchItineraryData();
  }, [city]);

  const formatDate = (date: any) => {
    const formattedDate = new Date(date.year, date.month - 1, date.day, date.hour, date.minute, date.second);
    return formattedDate.toLocaleString();
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p>Loading itinerary...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <Button variant="outline" className="mb-6" onClick={() => navigate(-1)}>
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
                  Your personalized travel plan
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
            {/* Hotel Information */}
            {hotel && (
              <div className="mb-8">
                <h3 className="text-xl font-semibold mb-4 flex items-center">
                  <Hotel className="mr-2 h-5 w-5 text-primary" />
                  Hotel Accommodation
                </h3>
                <Card className="p-4">
                  <p className="text-lg font-medium">{hotel.name}</p>
                  <p className="text-sm text-muted-foreground">Price per night: ${hotel.price}</p>
                </Card>
              </div>
            )}

            {/* Flight Information */}
            <div className="mb-8">
              <h3 className="text-xl font-semibold mb-4 flex items-center">
                <Plane className="mr-2 h-5 w-5 text-primary" />
                Flight Details
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {flights.go && (
                  <Card className="p-4">
                    <p className="font-semibold">Departure Flight</p>
                    <p className="text-sm text-muted-foreground">
                      {flights.go.origin} to {flights.go.destination}
                    </p>
                    <p className="text-sm text-muted-foreground">
                      Airline: {flights.go.airline}
                    </p>
                    <p className="text-sm text-muted-foreground">
                      Departure Time: {formatDate(flights.go.departure_time)}
                    </p>
                    <p className="text-sm text-muted-foreground">
                      Price: ${flights.go.price}
                    </p>
                  </Card>
                )}
                {flights.return && (
                  <Card className="p-4">
                    <p className="font-semibold">Return Flight</p>
                    <p className="text-sm text-muted-foreground">
                      {flights.return.origin} to {flights.return.destination}
                    </p>
                    <p className="text-sm text-muted-foreground">
                      Airline: {flights.return.airline}
                    </p>
                    <p className="text-sm text-muted-foreground">
                      Departure Time: {formatDate(flights.return.departure_time)}
                    </p>
                    <p className="text-sm text-muted-foreground">
                      Price: ${flights.return.price}
                    </p>
                  </Card>
                )}
              </div>
            </div>

            {/* Purchase Section */}
            <div className="mt-8 pt-6 border-t text-center">
              <h3 className="text-xl font-semibold mb-4 flex justify-center items-center">
                <ListCheck className="mr-2 h-5 w-5 text-primary" />
                Purchase Trip
              </h3>
              <p className="text-muted-foreground mb-6">
                Ready to enjoy an unforgettable experience in {city}? Book your trip now!
              </p>
              <Button onClick={() => navigate("/")}>
                Go to homepage
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Itinerary;
