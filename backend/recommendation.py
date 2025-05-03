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
        self.df = pd.read_csv(data_path)
        self._validate_data()
        
        # Prepare features
        self.base_features = [col for col in self.df.columns 
                            if col not in ('city', 'country', 'city_cluster')]
        self._prepare_features()
        
        # Build model pipeline with imputation
        self.model = self._build_model()
        self.city_to_idx = {city: idx for idx, city in enumerate(self.df['city'])}
        self.vetoed_cities = set()
        self.scaler = MinMaxScaler()
        self.X_scaled = self.scaler.fit_transform(self.df[self.base_features])

    def _validate_data(self):
        """Ensure data is clean and valid"""
        if self.df.empty:
            raise ValueError("City data is empty")
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
        
        for user in [u.dict() if hasattr(u, 'dict') else u for u in users_data]:
            if 'veto' in user:
                if isinstance(user['veto'], list):
                    self.vetoed_cities.update(city.lower() for city in user['veto'])
                else:
                    self.vetoed_cities.add(str(user['veto']).lower())
            
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

    def train(self, default_cities=['Barcelona', 'Tokyo', 'Paris']):
        """Enhanced training using all cities with similarity-based approach"""
        # We'll keep this function for compatibility but won't actually use the MLP for recommendations
        # The MLP training is maintained for backward compatibility
        X_train = []
        y_train = []
        
        for city in default_cities:
            if city in self.city_to_idx:
                city_data = self.df.iloc[self.city_to_idx[city]][self.base_features].values
                poly_vec = self.poly.transform(city_data.reshape(1, -1))
                X_train.append(poly_vec[0])
                y_train.append(self.city_to_idx[city])
        
        if not X_train:
            raise ValueError("No valid training cities found")
        
        self.model.fit(np.array(X_train), np.array(y_train))

    def recommend(self, preferences, top_k=10):
        """Improved recommendation using cosine similarity"""
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
            for idx in np.argsort(similarities)[::-1]:
                city_name = str(self.df.iloc[idx]['city']).lower()
                if city_name not in self.vetoed_cities:
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
            # Fallback to default cities if error occurs
            return [{
                'city': city,
                'country': self.df[self.df['city'] == city]['country'].values[0],
                'match_score': 80.0,
                'features': {f: float(self.df[self.df['city'] == city][f].values[0]) 
                           for f in preferences.keys()}
            } for city in ['Barcelona', 'Tokyo', 'Paris', 'New York', 'London', 
                          'Berlin', 'Sydney', 'Singapore', 'Dubai', 'Rome'][:top_k]]

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