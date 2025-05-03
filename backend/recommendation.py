import json
import numpy as np
import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import PolynomialFeatures, MinMaxScaler
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.metrics.pairwise import cosine_similarity
import warnings

# Suppress warnings
warnings.filterwarnings('ignore')

class RobustCityRecommender:
    def __init__(self, data_path):
        # Load and validate city data
        self.df = pd.read_csv(data_path, encoding='latin1')
        
        # Load and filter cities from location.csv
        location_df = pd.read_csv('location.csv', encoding='latin1')
        self.df = self.df[self.df['city'].isin(location_df['City'])]
            
        self._validate_data()
        
        # Prepare features
        self.base_features = [col for col in self.df.columns 
                            if col not in ('city', 'country', 'city_cluster')]
        self._prepare_features()
        
        # Build model pipeline with imputation
        self.model = self._build_model()
        self.city_to_idx = {city: idx for idx, city in enumerate(self.df['city'])}
        self.vetoed_cities = set()
        self.favoured_city = None  # New attribute to store favoured city
        self.scaler = MinMaxScaler()
        self.X_scaled = self.scaler.fit_transform(self.df[self.base_features])

    def _validate_data(self):
        """Ensure data is clean and valid"""
        if self.df.empty:
            raise ValueError("City data is empty after filtering with location.csv")
        if self.df.isnull().values.any():
            self.df = self.df.fillna(self.df.median())

    def _prepare_features(self):
        """Create polynomial features with imputation"""
        self.poly = PolynomialFeatures(degree=2, interaction_only=True, include_bias=False)
        self.X = self.poly.fit_transform(self.df[self.base_features])
        self.feature_names = [str(f) for f in self.poly.get_feature_names_out(self.base_features)]

    def _build_model(self):
        """Build robust pipeline with imputation"""
        return make_pipeline(
            SimpleImputer(strategy='median'),
            MinMaxScaler(),
            MLPClassifier(
                hidden_layer_sizes=(128, 64),
                early_stopping=True,
                max_iter=500,
                random_state=42
            )
        )

    def calculate_aggregate_preferences(self, users_data):
        """Calculate weighted mean preferences safely"""
        agg_prefs = {feat: [] for feat in self.base_features}
        self.vetoed_cities = set()
        self.favoured_city = None  # Reset favoured city
        
        for user in [u.dict() if hasattr(u, 'dict') else u for u in users_data]:
            if 'veto' in user:
                if isinstance(user['veto'], list):
                    self.vetoed_cities.update(city.lower() for city in user['veto'])
                else:
                    self.vetoed_cities.add(str(user['veto']).lower())
            
            if 'favoured' in user:  # Check for favoured city
                self.favoured_city = str(user['favoured']).lower()
            
            try:
                user_total = max(sum(tag['score'] for tag in user['tags']), 1e-6)
                for tag in user['tags']:
                    if tag['tag'] in agg_prefs:
                        agg_prefs[tag['tag']].append(tag['score'] / user_total)
            except Exception as e:
                print(f"Warning: Error processing user {user.get('user', 'unknown')}: {e}")
                continue
        
        final_prefs = {}
        for feat, values in agg_prefs.items():
            if values:
                final_prefs[feat] = np.nanmean(values) if values else 0
        return final_prefs

    def train(self, default_cities=None):
        """Train using all cities from location.csv"""
        # Use all available cities for training
        X_train = self.X
        y_train = np.arange(len(self.df))  # Each city is its own class
        
        self.model.fit(X_train, y_train)

    def recommend(self, preferences, top_k=10):
        """Get top 10 recommendations from location.csv with favoured city prioritization"""
        try:
            # Create user preference vector
            user_vec = np.array([preferences.get(feat, 0) for feat in self.base_features])
            
            # Normalize user vector
            user_vec = user_vec / (np.linalg.norm(user_vec) + 1e-8)
            
            # Calculate cosine similarity with all cities
            similarities = cosine_similarity(
                user_vec.reshape(1, -1), 
                self.X_scaled
            )[0]
            
            # Get top recommendations excluding vetoed cities
            recommendations = []
            favoured_city_added = False
            
            # First check if favoured city exists and should be added
            if self.favoured_city:
                favoured_idx = None
                for idx, city in enumerate(self.df['city']):
                    if str(city).lower() == self.favoured_city:
                        favoured_idx = idx
                        break
                
                if favoured_idx is not None and self.favoured_city not in self.vetoed_cities:
                    recommendations.append({
                        'city': self.df.iloc[favoured_idx]['city'],
                        'country': self.df.iloc[favoured_idx]['country'],
                        'match_score': 100.0,  # Max score for favoured city
                        'features': {f: float(self.df.iloc[favoured_idx][f]) for f in preferences.keys()}
                    })
                    favoured_city_added = True
            
            # Add other cities
            for idx in np.argsort(similarities)[::-1]:
                city_name = str(self.df.iloc[idx]['city']).lower()
                if (city_name not in self.vetoed_cities and 
                    (not favoured_city_added or city_name != self.favoured_city)):
                    recommendations.append({
                        'city': self.df.iloc[idx]['city'],
                        'country': self.df.iloc[idx]['country'],
                        'match_score': round(float(similarities[idx] * 100), 1),
                        'features': {f: float(self.df.iloc[idx][f]) for f in preferences.keys()}
                    })
                    if len(recommendations) >= top_k:
                        break
            
            return recommendations
        
        except Exception as e:
            print(f"Recommendation error: {e}")
            # Fallback to random cities from location.csv
            location_df = pd.read_csv('location.csv', encoding='latin1')
            fallback_cities = location_df['City'].sample(min(10, len(location_df))).tolist()
            
            # Include favoured city in fallback if specified
            if self.favoured_city:
                fallback_cities = [self.favoured_city.title()] + [
                    c for c in fallback_cities if c.lower() != self.favoured_city
                ][:top_k-1]
            
            return [{
                'city': city,
                'country': location_df[location_df['City'] == city]['Country'].values[0],
                'match_score': 80.0,
                'features': {f: float(self.df[self.df['city'] == city][f].values[0]) 
                           if city in self.city_to_idx else 0
                           for f in preferences.keys()}
            } for city in fallback_cities[:top_k]]

def generate_recommendations(users_data):
    """Main function to generate recommendations"""
    print("Initializing recommendation system...")
    
    try:
        recommender = RobustCityRecommender('backend/data/enhanced_cities.csv')
        
        print("Training model...")
        recommender.train()
        print("Model trained successfully!")
        
        print("Calculating aggregate preferences...")
        agg_prefs = recommender.calculate_aggregate_preferences(users_data)
        
        print("Generating recommendations...")
        results = recommender.recommend(agg_prefs, top_k=10)
        
        if not results:
            raise ValueError("No recommendations generated")
        
        output = {
            "aggregate_preferences": {k: float(v) for k, v in agg_prefs.items()},
            "vetoed_cities": list(recommender.vetoed_cities),
            "top_recommendations": results
        }
        
        print("Recommendations:")
        print(json.dumps(output, indent=2))

        with open('output.json', 'w') as f:
            json.dump(output, f, indent=2)
        
        print("Successfully saved recommendations to output.json")
        return True
    
    except Exception as e:
        print(f"Fatal error: {e}")
        return False

if __name__ == "__main__":
    generate_recommendations()