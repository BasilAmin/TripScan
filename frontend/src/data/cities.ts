
export interface City {
  id: string;
  name: string;
  code: string;
  country: string;
}

export const popularCities: City[] = [
  { id: '1', name: 'London', code: 'LHR', country: 'United Kingdom' },
  { id: '2', name: 'New York', code: 'JFK', country: 'United States' },
  { id: '3', name: 'Paris', code: 'CDG', country: 'France' },
  { id: '4', name: 'Tokyo', code: 'NRT', country: 'Japan' },
  { id: '5', name: 'Dubai', code: 'DXB', country: 'United Arab Emirates' },
  { id: '6', name: 'Barcelona', code: 'BCN', country: 'Spain' },
  { id: '7', name: 'Rome', code: 'FCO', country: 'Italy' },
  { id: '8', name: 'Amsterdam', code: 'AMS', country: 'Netherlands' },
  { id: '9', name: 'Sydney', code: 'SYD', country: 'Australia' },
  { id: '10', name: 'Singapore', code: 'SIN', country: 'Singapore' },
  { id: '11', name: 'Hong Kong', code: 'HKG', country: 'China' },
  { id: '12', name: 'San Francisco', code: 'SFO', country: 'United States' },
  { id: '13', name: 'Los Angeles', code: 'LAX', country: 'United States' },
  { id: '14', name: 'Toronto', code: 'YYZ', country: 'Canada' },
  { id: '15', name: 'Berlin', code: 'TXL', country: 'Germany' },
  { id: '16', name: 'Bangkok', code: 'BKK', country: 'Thailand' },
  { id: '17', name: 'Istanbul', code: 'IST', country: 'Turkey' },
  { id: '18', name: 'Moscow', code: 'SVO', country: 'Russia' },
  { id: '19', name: 'Rio de Janeiro', code: 'GIG', country: 'Brazil' },
  { id: '20', name: 'Buenos Aires', code: 'EZE', country: 'Argentina' },
  { id: '21', name: 'Cairo', code: 'CAI', country: 'Egypt' },
  { id: '22', name: 'Seoul', code: 'ICN', country: 'South Korea' },
  { id: '23', name: 'Mumbai', code: 'BOM', country: 'India' },
  { id: '24', name: 'Lima', code: 'LIM', country: 'Peru' },
  { id: '25', name: 'Kuala Lumpur', code: 'KUL', country: 'Malaysia' },
  { id: '26', name: 'Santiago', code: 'SCL', country: 'Chile' },
  { id: '27', name: 'Lisbon', code: 'LIS', country: 'Portugal' },
  { id: '28', name: 'Vienna', code: 'VIE', country: 'Austria' },
  { id: '29', name: 'Brussels', code: 'BRU', country: 'Belgium' },
  { id: '30', name: 'Stockholm', code: 'ARN', country: 'Sweden' },
  { id: '31', name: 'Oslo', code: 'OSL', country: 'Norway' },
  { id: '32', name: 'Helsinki', code: 'HEL', country: 'Finland' },
  { id: '33', name: 'Copenhagen', code: 'CPH', country: 'Denmark' },
  { id: '34', name: 'Dublin', code: 'DUB', country: 'Ireland' },
  { id: '35', name: 'Athens', code: 'ATH', country: 'Greece' },
  { id: '36', name: 'Budapest', code: 'BUD', country: 'Hungary' },
  { id: '37', name: 'Nairobi', code: 'NBO', country: 'Kenya' },
  { id: '38', name: 'Manila', code: 'MNL', country: 'Philippines' },
  { id: '39', name: 'Jakarta', code: 'CGK', country: 'Indonesia' }
];

export const getAllCities = (): City[] => {
  return popularCities;
};

export const searchCities = (query: string): City[] => {
  if (!query) return [];
  const lowercaseQuery = query.toLowerCase();
  
  return popularCities.filter(city => 
    city.name.toLowerCase().includes(lowercaseQuery) || 
    city.code.toLowerCase().includes(lowercaseQuery) ||
    city.country.toLowerCase().includes(lowercaseQuery)
  ).slice(0, 5);
};
