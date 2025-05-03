import pandas as pd
import numpy as np
from faker import Faker
from sklearn.cluster import KMeans

def generate_realistic_city_data(num_cities=100):
    fake = Faker()
    
    # Realistic city profiles with accurate feature scores
    city_profiles = {
        # European cities
        'Barcelona': {'food': 9, 'hiking': 6, 'english_friendly': 6, 'nightlife': 9, 'culture': 9},
        'Paris': {'food': 10, 'hiking': 3, 'english_friendly': 5, 'nightlife': 8, 'culture': 10},
        'London': {'food': 8, 'hiking': 4, 'english_friendly': 10, 'nightlife': 8, 'culture': 9},
        
        # Asian cities
        'Tokyo': {'food': 10, 'hiking': 7, 'english_friendly': 4, 'nightlife': 8, 'culture': 10},
        'Singapore': {'food': 9, 'hiking': 2, 'english_friendly': 9, 'nightlife': 7, 'culture': 7},
        
        # North American cities
        'New York': {'food': 10, 'hiking': 5, 'english_friendly': 10, 'nightlife': 9, 'culture': 9},
        'Vancouver': {'food': 7, 'hiking': 9, 'english_friendly': 10, 'nightlife': 6, 'culture': 7},
        
        # Oceania
        'Sydney': {'food': 8, 'hiking': 7, 'english_friendly': 10, 'nightlife': 7, 'culture': 8}
    }
    
    # Additional features with realistic distributions
    additional_features = [
        'safety', 'affordability', 'public_transit', 
        'walkability', 'cleanliness', 'beaches'
    ]
    
    data = []
    for city, features in city_profiles.items():
        # Add realistic values for additional features
        features.update({
            'safety': np.random.randint(7, 10),
            'affordability': np.random.randint(3, 8),
            'public_transit': np.random.randint(6, 10),
            'walkability': np.random.randint(5, 9),
            'cleanliness': np.random.randint(6, 9),
            'beaches': np.random.randint(1, 10) if city in ['Barcelona', 'Sydney'] else np.random.randint(1, 5)
        })
        
        data.append({
            'city': city,
            'country': 'Spain' if city == 'Barcelona' else \
                      'France' if city == 'Paris' else \
                      'UK' if city == 'London' else \
                      'Japan' if city == 'Tokyo' else \
                      'Singapore' if city == 'Singapore' else \
                      'USA' if city == 'New York' else \
                      'Canada' if city == 'Vancouver' else 'Australia',
            **features
        })
    
    # Add some random cities to fill out the dataset
    for _ in range(num_cities - len(city_profiles)):
        city = fake.city()
        data.append({
            'city': city,
            'country': fake.country(),
            'food': np.random.randint(3, 9),
            'hiking': np.random.randint(2, 9),
            'english_friendly': np.random.randint(2, 9),
            'nightlife': np.random.randint(3, 9),
            'culture': np.random.randint(4, 9),
            'safety': np.random.randint(5, 9),
            'affordability': np.random.randint(2, 8),
            'public_transit': np.random.randint(3, 8),
            'walkability': np.random.randint(4, 8),
            'cleanliness': np.random.randint(5, 9),
            'beaches': np.random.randint(1, 7)
        })
    
    df = pd.DataFrame(data)
    
    # Add cluster-based features
    kmeans = KMeans(n_clusters=5)
    features_for_clustering = ['food', 'hiking', 'english_friendly', 'nightlife', 'culture']
    clusters = kmeans.fit_predict(df[features_for_clustering])
    df['city_cluster'] = clusters
    
    return df

if __name__ == "__main__":
    city_data = generate_realistic_city_data()
    city_data.to_csv('realistic_cities.csv', index=False)
    print("Generated realistic city data with shape:", city_data.shape)