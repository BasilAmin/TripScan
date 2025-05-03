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

class CityRecommender:
    def __init__(self, data_path):
        # Load city data
        self.df = pd.read_csv(data_path)
        
        # Validate and clean data
        if self.df.empty:
            raise ValueError("City data is empty")
        self.df = self.df.fillna(self.df.median())
        
        # Prepare features
        self.base_features = [col for col in self.df.columns 
                            if col not in ('city', 'country', 'city_cluster')]
        self.poly = PolynomialFeatures(degree=2, interaction_only=True, include_bias=False)
        self.X = self.poly.fit_transform(self.df[self.base_features])
        
        # Build model pipeline
        self.model = make_pipeline(
            SimpleImputer(strategy='median'),
            MinMaxScaler(),
            MLPClassifier(
                hidden_layer_sizes=(128, 64),
                early_stopping=True,
                max_iter=500,
                random_state=42
            )
        )
        
        # Create city index (case insensitive)
        self.city_to_idx = {str(city).lower(): idx for idx, city in enumerate(self.df['city'])}

    def process_users(self, users_data):
        """Process user data and return (preferences, vetoes)"""
        agg_prefs = {feat: [] for feat in self.base_features}
        vetoes = set()
        
        for user in users_data:
            # Process vetoes
            if 'veto' in user:
                if isinstance(user['veto'], list):
                    vetoes.update(str(city).lower() for city in user['veto'])
                else:
                    vetoes.add(str(user['veto']).lower())
            
            # Process preferences
            user_total = max(sum(tag['score'] for tag in user['tags']), 1e-6)
            for tag in user['tags']:
                if tag['tag'] in agg_prefs:
                    agg_prefs[tag['tag']].append(tag['score'] / user_total)
        
        # Calculate mean preferences
        preferences = {k: np.mean(v) for k, v in agg_prefs.items() if v}
        return preferences, vetoes

    def train(self, training_cities=['barcelona', 'tokyo', 'paris']):
        """Train model on representative cities"""
        X_train = []
        y_train = []
        
        for city in training_cities:
            if city in self.city_to_idx:
                idx = self.city_to_idx[city]
                city_data = self.df.iloc[idx][self.base_features].values
                poly_vec = self.poly.transform(city_data.reshape(1, -1))
                X_train.append(poly_vec[0])
                y_train.append(idx)
        
        if not X_train:
            raise ValueError("No valid training cities found")
        
        self.model.fit(np.array(X_train), np.array(y_train))

    def recommend(self, preferences, vetoes=None, top_k=3):
        """Generate recommendations excluding vetoed cities"""
        if vetoes is None:
            vetoes = set()
        
        # Create input vector
        vec = np.zeros(len(self.base_features))
        for feat, score in preferences.items():
            if feat in self.base_features:
                vec[self.base_features.index(feat)] = score
        
        # Get predictions
        poly_vec = self.poly.transform(vec.reshape(1, -1))
        probas = self.model.predict_proba(poly_vec)[0]
        
        # Create list of (index, score) pairs excluding vetoed cities
        valid_cities = []
        for idx in range(len(probas)):
            city_name = str(self.df.iloc[idx]['city']).lower()
            if city_name not in vetoes:
                valid_cities.append((idx, probas[idx]))
        
        if not valid_cities:
            raise ValueError("All potential recommendations were vetoed")
        
        # Sort by score and get top recommendations
        valid_cities.sort(key=lambda x: x[1], reverse=True)
        top_indices = [x[0] for x in valid_cities[:top_k]]
        
        return [{
            'city': self.df.iloc[idx]['city'],
            'country': self.df.iloc[idx]['country'],
            'match_score': round(float(probas[idx] * 100), 1),
            'features': {f: float(self.df.iloc[idx][f]) for f in preferences.keys()}
        } for idx in top_indices]

def main(input_path='input.json', output_path='output.json'):
    try:
        # Initialize recommender
        recommender = CityRecommender('location.csv')
        
        # Load and process input data
        with open(input_path) as f:
            users_data = json.load(f)
        
        # Calculate preferences and vetoes
        preferences, vetoes = recommender.process_users(users_data)
        
        # Train model
        recommender.train()
        
        # Generate recommendations
        results = recommender.recommend(preferences, vetoes)
        
        # Prepare output
        output = {
            "aggregate_preferences": preferences,
            "vetoed_cities": list(vetoes),
            "recommendations": results
        }
        
        # Save output
        with open(output_path, 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"Successfully generated recommendations in {output_path}")
        return True
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    main()