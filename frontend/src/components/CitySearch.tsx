
import { useState, useRef, useEffect } from 'react';
import { Command, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList } from "@/components/ui/command";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { Button } from "@/components/ui/button";
import { Check, MapPin } from "lucide-react";
import { City, searchCities } from '@/data/cities';
import { cn } from '@/lib/utils';

interface CitySearchProps {
  value: City | null;
  onChange: (city: City) => void;
  placeholder?: string;
}

const CitySearch = ({ value, onChange, placeholder = "Search cities..." }: CitySearchProps) => {
  const [open, setOpen] = useState(false);
  const [search, setSearch] = useState("");
  const [results, setResults] = useState<City[]>([]);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (search.length > 1) {
      const cities = searchCities(search);
      setResults(cities);
    } else {
      setResults([]);
    }
  }, [search]);

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button 
          variant="outline" 
          role="combobox" 
          aria-expanded={open}
          className="w-full justify-between border-none shadow-sm hover:bg-gray-50  text-gray-500"
        >
          {value ? (
            <div className="flex items-center gap-2 ">
              <MapPin className="h-4 w-4 text-muted-foreground" />
              <span>{value.name}</span>
              <span className="text-xs text-muted-foreground">({value.code})</span>
            </div>
          ) : (
            <div className="flex items-center gap-2">
              <MapPin className="h-4 w-4 text-muted-foreground" />
              <span className="text-muted-foreground">{placeholder}</span>
            </div>
          )}
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-full p-0" align="start">
        <Command>
          <CommandInput 
            placeholder={placeholder}
            value={search}
            onValueChange={setSearch}
            ref={inputRef}
            className="h-9"
          />
          <CommandList>
            <CommandEmpty>No cities found.</CommandEmpty>
            <CommandGroup>
              {results.map((city) => (
                <CommandItem
                  key={city.id}
                  value={city.name}
                  onSelect={() => {
                    onChange(city);
                    setOpen(false);
                    setSearch("");
                  }}
                  className="cursor-pointer"
                >
                  <div className="flex items-center justify-between w-full">
                    <div className="flex items-center gap-2">
                      <MapPin className="h-4 w-4 text-muted-foreground" />
                      <span>{city.name}</span>
                      <span className="text-xs text-muted-foreground">({city.code})</span>
                    </div>
                    <span className="text-xs text-muted-foreground">{city.country}</span>
                  </div>
                  <Check
                    className={cn(
                      "ml-auto h-4 w-4",
                      value?.id === city.id ? "opacity-100" : "opacity-0"
                    )}
                  />
                </CommandItem>
              ))}
            </CommandGroup>
          </CommandList>
        </Command>
      </PopoverContent>
    </Popover>
  );
};

export default CitySearch;
