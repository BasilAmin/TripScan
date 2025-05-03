
import { useState } from 'react';
import { DateRange } from "react-day-picker";
import { Button } from "@/components/ui/button";
import { City } from '@/data/cities';
import CitySearch from './CitySearch';
import DateRangePicker from './DateRangePicker';
import { Plane } from "lucide-react";

const TravelBanner = () => {
  const [origin, setOrigin] = useState<City | null>(null);
  const [dateRange, setDateRange] = useState<DateRange | undefined>({
    from: new Date(),
    to: undefined,
  });

  const handleSearch = () => {
    console.log('Search with:', { origin, dateRange });
    // In a real app, this would trigger a search or redirect
  };

  const isSearchDisabled = !origin || !dateRange?.from;

  return (
    <div className="w-full travel-gradient rounded-xl p-8 text-white shadow-lg">
      <h1 className="text-3xl font-bold mb-6 text-center">Explore the World Together</h1>
      <div className="bg-white p-4 rounded-lg shadow-md">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Origin City</label>
            <CitySearch value={origin} onChange={setOrigin} placeholder="Where are you flying from?" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Travel Dates</label>
            <DateRangePicker dateRange={dateRange} onDateRangeChange={setDateRange} />
          </div>
        </div>
        <div className="mt-6 flex justify-center">
          <Button 
            onClick={handleSearch} 
            disabled={isSearchDisabled}
            className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-8 rounded-full w-full md:w-auto"
          >
            <Plane className="mr-2 h-4 w-4" />
            Find Flights
          </Button>
        </div>
      </div>
    </div>
  );
};

export default TravelBanner;
