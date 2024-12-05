from abc import ABC, abstractmethod
from typing import List, Union, Dict
import pandas as pd
import numpy as np

class BaseRecommender(ABC):
    """Base class for recommender systems."""
    
    def __init__(self):
        self.is_fitted = False
        
    @abstractmethod
    def fit(self, data: pd.DataFrame) -> 'BaseRecommender':
        """
        Fit the model to training data.
        
        Args:
            data: DataFrame containing user-item interactions
            
        Returns:
            self: The fitted model
        """
        pass
    
    @abstractmethod
    def recommend_items(
        self, 
        user_ids: Union[List[int], np.ndarray], 
        n_items: int = 10,
        exclude_seen: bool = True
    ) -> pd.DataFrame:
        """
        Generate recommendations for users.
        
        Args:
            user_ids: List of user IDs to generate recommendations for
            n_items: Number of recommendations per user
            exclude_seen: Whether to exclude items the user has already interacted with
            
        Returns:
            DataFrame with user-item-score recommendations
        """
        pass
    
    def _validate_not_fitted(self):
        """Check if the model is not already fitted."""
        if self.is_fitted:
            raise ValueError("Model is already fitted. Call 'fit' with new data to refit the model.")
    
    def _validate_is_fitted(self):
        """Check if the model is fitted before making predictions."""
        if not self.is_fitted:
            raise ValueError("Model is not fitted yet. Call 'fit' before making predictions.")
