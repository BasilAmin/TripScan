import json
import numpy as np
import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import PolynomialFeatures, MinMaxScaler
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
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
        
        for user in users_data:
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
        """Train with default cities to ensure stability"""
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
        """Get recommendations with veto handling"""
        try:
            vec = np.zeros(len(self.base_features))
            for feat, score in preferences.items():
                if feat in self.base_features:
                    vec[self.base_features.index(feat)] = score
            
            vec = np.nan_to_num(vec)
            poly_vec = self.poly.transform(vec.reshape(1, -1))
            probas = self.model.predict_proba(poly_vec)[0]
            
            recommendations = []
            for idx in np.argsort(probas)[::-1]:
                city_name = str(self.df.iloc[idx]['city']).lower()
                if city_name not in self.vetoed_cities:
                    recommendations.append({
                        'city': self.df.iloc[idx]['city'],
                        'country': self.df.iloc[idx]['country'],
                        'match_score': round(float(probas[idx] * 100), 1),
                        'features': {f: float(self.df.iloc[idx][f]) for f in preferences.keys()}
                    })
                    if len(recommendations) >= top_k:
                        break
            
            return recommendations
        
        except Exception as e:
            print(f"Recommendation error: {e}")
            return []

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
        results = recommender.recommend(agg_prefs)
        
        if not results:
            raise ValueError("No recommendations generated")
        
        output = {
            "aggregate_preferences": {k: float(v) for k, v in agg_prefs.items()},
            "vetoed_cities": list(recommender.vetoed_cities),
            "top_recommendations": results
        }
        
        with open('output.json', 'w') as f:
            json.dump(output, f, indent=2)
        
        print("Successfully saved recommendations to output.json")
        return True
    
    except Exception as e:
        print(f"Fatal error: {e}")
        return False

if __name__ == "__main__":
    generate_recommendations()