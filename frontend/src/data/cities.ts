
export interface City {
  id: string;
  name: string;
  code: string;
  country: string;
}

export const popularCities: City[] = [
  { id: '1', name: 'London', code: 'LON', country: 'United Kingdom' },
  { id: '2', name: 'New York', code: 'NYC', country: 'United States' },
  { id: '3', name: 'Paris', code: 'PAR', country: 'France' },
  { id: '4', name: 'Tokyo', code: 'TYO', country: 'Japan' },
  { id: '5', name: 'Dubai', code: 'DXB', country: 'United Arab Emirates' },
  { id: '6', name: 'Barcelona', code: 'BCN', country: 'Spain' },
  { id: '7', name: 'Rome', code: 'ROM', country: 'Italy' },
  { id: '8', name: 'Amsterdam', code: 'AMS', country: 'Netherlands' },
  { id: '9', name: 'Sydney', code: 'SYD', country: 'Australia' },
  { id: '10', name: 'Singapore', code: 'SIN', country: 'Singapore' },
  { id: '11', name: 'Hong Kong', code: 'HKG', country: 'China' },
  { id: '12', name: 'San Francisco', code: 'SFO', country: 'United States' },
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
