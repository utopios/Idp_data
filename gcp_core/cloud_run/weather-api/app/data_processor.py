import pandas as pd
import numpy as np
from datetime import datetime

class WeatherDataProcessor:
    def __init__(self, df):
        """
        Initialise le processeur avec un DataFrame pandas
        """
        self.df = df.copy()
        self._prepare_data()
    
    def _prepare_data(self):
        """Prépare les données : conversion de types, tri, etc."""
        self.df['date'] = pd.to_datetime(self.df['date'])
        self.df = self.df.sort_values('date')
        
        # Colonnes numériques
        self.numeric_columns = ['temperature', 'humidity', 'pressure', 
                                'wind_speed', 'precipitation']
    
    def get_global_statistics(self, start_date=None, end_date=None):
        """Calcule les statistiques globales"""
        df = self._filter_by_date(start_date, end_date)
        
        stats = {}
        for col in self.numeric_columns:
            stats[col] = {
                'mean': float(df[col].mean()),
                'min': float(df[col].min()),
                'max': float(df[col].max()),
                'std': float(df[col].std()),
                'median': float(df[col].median())
            }
        
        stats['total_precipitation'] = float(df['precipitation'].sum())
        stats['records_count'] = len(df)
        
        return stats
    
    def get_monthly_summary(self, year):
        """Résumé mensuel pour une année"""
        df = self.df[self.df['date'].dt.year == year]
        
        monthly = df.groupby(df['date'].dt.month).agg({
            'temperature': 'mean',
            'precipitation': 'sum',
            'humidity': 'mean',
            'wind_speed': 'mean'
        }).round(2)
        
        # Compter les jours de pluie
        rain_days = df[df['precipitation'] > 0].groupby(
            df['date'].dt.month
        ).size()
        
        result = []
        for month in range(1, 13):
            if month in monthly.index:
                result.append({
                    'month': month,
                    'avg_temperature': float(monthly.loc[month, 'temperature']),
                    'total_precipitation': float(monthly.loc[month, 'precipitation']),
                    'avg_humidity': float(monthly.loc[month, 'humidity']),
                    'avg_wind_speed': float(monthly.loc[month, 'wind_speed']),
                    'days_with_rain': int(rain_days.get(month, 0))
                })
        
        return result
    
    def detect_anomalies(self, threshold=3):
        """
        Détecte les anomalies en utilisant le z-score
        threshold: nombre d'écarts-types pour considérer une valeur comme anomale
        """
        anomalies = []
        
        for col in self.numeric_columns:
            mean = self.df[col].mean()
            std = self.df[col].std()
            
            z_scores = np.abs((self.df[col] - mean) / std)
            anomaly_mask = z_scores > threshold
            
            anomaly_records = self.df[anomaly_mask]
            
            for idx, row in anomaly_records.iterrows():
                z_score = z_scores[idx]
                anomalies.append({
                    'date': row['date'].strftime('%Y-%m-%d'),
                    'variable': col,
                    'value': float(row[col]),
                    'mean': float(mean),
                    'std': float(std),
                    'z_score': float(z_score),
                    'severity': 'high' if z_score > 4 else 'medium'
                })
        
        return sorted(anomalies, key=lambda x: x['z_score'], reverse=True)
    
    def get_correlation_matrix(self):
        """Calcule la matrice de corrélation"""
        corr = self.df[self.numeric_columns].corr()
        
        result = {}
        for i, col1 in enumerate(self.numeric_columns):
            for col2 in self.numeric_columns[i+1:]:
                key = f"{col1}_{col2}"
                result[key] = round(float(corr.loc[col1, col2]), 3)
        
        return result
    
    def _filter_by_date(self, start_date=None, end_date=None):
        """Filtre le DataFrame par dates"""
        df = self.df.copy()
        
        if start_date:
            df = df[df['date'] >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df['date'] <= pd.to_datetime(end_date)]
        
        return df