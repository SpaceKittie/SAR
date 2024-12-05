import numpy as np
import pandas as pd
from scipy import sparse
from typing import Optional, List, Union
from .base import BaseRecommender

class SARModel(BaseRecommender):
    """
    Sequential Action Rules (SAR) recommender system.
    
    This implementation follows the core principles of the SAR algorithm:
    1. Build an item-to-item similarity matrix based on co-occurrence
    2. Apply time decay to give more weight to recent interactions
    3. Generate recommendations using matrix operations
    
    Args:
        similarity_type: Type of similarity to use ('jaccard' or 'lift')
        time_decay_coefficient: Coefficient for time decay function
        time_now: Reference time for decay calculation
        timedecay_formula: Whether to use time decay in similarity calculation
    """
    
    def __init__(
        self,
        similarity_type: str = 'jaccard',
        time_decay_coefficient: float = 30,
        time_now: Optional[float] = None,
        timedecay_formula: bool = True
    ):
        super().__init__()
        self.similarity_type = similarity_type
        self.time_decay_coefficient = time_decay_coefficient
        self.time_now = time_now
        self.timedecay_formula = timedecay_formula
        
        self.user_items = None
        self.item_similarity = None
        self.item_means = None
        self.user_ids = None
        self.item_ids = None
        
    def _prepare_data(self, data: pd.DataFrame) -> sparse.csr_matrix:
        """
        Convert interaction data to sparse user-item matrix.
        
        Args:
            data: DataFrame with columns ['UserId', 'ItemId', 'Rating', 'Timestamp']
            
        Returns:
            Sparse matrix of user-item interactions
        """
        # Store unique IDs for later use
        self.user_ids = data['UserId'].unique()
        self.item_ids = data['ItemId'].unique()
        
        # Create mappings for efficient matrix operations
        self.user_map = {uid: idx for idx, uid in enumerate(self.user_ids)}
        self.item_map = {iid: idx for idx, iid in enumerate(self.item_ids)}
        
        # Map IDs to indices
        user_idx = data['UserId'].map(self.user_map)
        item_idx = data['ItemId'].map(self.item_map)
        
        # Apply time decay if enabled
        if self.timedecay_formula and 'Timestamp' in data.columns:
            if self.time_now is None:
                self.time_now = data['Timestamp'].max()
            
            time_diff = (self.time_now - data['Timestamp']) / (24 * 60 * 60)  # Convert to days
            ratings = data['Rating'] * np.exp(-self.time_decay_coefficient * time_diff)
        else:
            ratings = data['Rating']
            
        # Create sparse matrix
        return sparse.csr_matrix(
            (ratings, (user_idx, item_idx)),
            shape=(len(self.user_ids), len(self.item_ids))
        )
        
    def _compute_similarity(self, user_items: sparse.csr_matrix) -> sparse.csr_matrix:
        """
        Compute item-item similarity matrix.
        
        Args:
            user_items: Sparse user-item interaction matrix
            
        Returns:
            Sparse item-item similarity matrix
        """
        if self.similarity_type == 'jaccard':
            # Compute co-occurrence matrix
            item_co_occurrence = user_items.T @ user_items
            
            # Compute item occurrence frequencies
            item_frequencies = np.array(user_items.sum(axis=0)).flatten()
            
            # Compute Jaccard similarity
            similarity = item_co_occurrence.multiply(
                1 / (item_frequencies[:, None] + item_frequencies[None, :] - item_co_occurrence)
            )
            
        elif self.similarity_type == 'lift':
            # Compute item probabilities
            item_probs = np.array(user_items.sum(axis=0) / user_items.shape[0]).flatten()
            
            # Compute co-occurrence probabilities
            co_occurrence_probs = (user_items.T @ user_items) / user_items.shape[0]
            
            # Compute lift
            similarity = co_occurrence_probs.multiply(
                1 / (item_probs[:, None] @ item_probs[None, :])
            )
            
        else:
            raise ValueError(f"Unknown similarity type: {self.similarity_type}")
            
        return similarity.tocsr()
        
    def fit(self, data: pd.DataFrame) -> 'SARModel':
        """
        Fit the SAR model to training data.
        
        Args:
            data: DataFrame with columns ['UserId', 'ItemId', 'Rating', 'Timestamp']
            
        Returns:
            self: The fitted model
        """
        self._validate_not_fitted()
        
        # Prepare user-item matrix
        self.user_items = self._prepare_data(data)
        
        # Compute item similarity matrix
        self.item_similarity = self._compute_similarity(self.user_items)
        
        # Compute item means for scaling
        self.item_means = np.array(self.user_items.sum(axis=0) / 
                                 (self.user_items != 0).sum(axis=0)).flatten()
        
        self.is_fitted = True
        return self
        
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
            DataFrame with columns ['UserId', 'ItemId', 'Score']
        """
        self._validate_is_fitted()
        
        # Convert user IDs to internal indices
        user_indices = [self.user_map[uid] for uid in user_ids]
        
        # Get user profiles
        user_profiles = self.user_items[user_indices]
        
        # Generate scores
        scores = user_profiles @ self.item_similarity
        
        if exclude_seen:
            # Set scores of seen items to large negative value
            seen_mask = user_profiles.nonzero()
            scores[seen_mask[0], seen_mask[1]] = -np.inf
            
        # Get top-k items
        n_users = len(user_indices)
        top_items = np.zeros((n_users, n_items), dtype=np.int32)
        top_scores = np.zeros((n_users, n_items))
        
        for i, score in enumerate(scores):
            score_array = score.toarray().ravel()  # Convert sparse matrix to dense array
            top_idx = np.argpartition(score_array, -n_items)[-n_items:]
            top_idx = top_idx[np.argsort(-score_array[top_idx])]
            top_items[i] = top_idx
            top_scores[i] = score_array[top_idx]
            
        # Create recommendations DataFrame
        recommendations = pd.DataFrame({
            'UserId': np.repeat(user_ids, n_items),
            'ItemId': [self.item_ids[idx] for idx in top_items.flatten()],
            'Score': top_scores.flatten()
        })
        
        # Normalize scores to 0-1 range for each user
        recommendations['Score'] = recommendations.groupby('UserId')['Score'].transform(
            lambda x: (x - x.min()) / (x.max() - x.min()) if x.max() != x.min() else x
        )
        
        return recommendations
