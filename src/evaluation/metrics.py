from typing import List, Optional
import numpy as np
import pandas as pd
from sklearn.metrics import ndcg_score

def precision_at_k(
    y_true: pd.DataFrame,
    y_pred: pd.DataFrame,
    k: int,
    user_col: str = 'UserId',
    item_col: str = 'ItemId'
) -> float:
    """
    Calculate Precision@K for recommendations.
    
    Args:
        y_true: DataFrame of ground truth interactions
        y_pred: DataFrame of recommendations
        k: Number of recommendations to consider
        user_col: Name of user ID column
        item_col: Name of item ID column
        
    Returns:
        Precision@K score
    """
    # Group predictions by user and get top k
    user_recs = y_pred.groupby(user_col).head(k)
    
    # Create set of true user-item interactions
    true_interactions = set(
        zip(y_true[user_col].values, y_true[item_col].values)
    )
    
    # Calculate hits
    hits = sum(
        1 for _, row in user_recs.iterrows()
        if (row[user_col], row[item_col]) in true_interactions
    )
    
    return hits / (len(user_recs) * k)

def recall_at_k(
    y_true: pd.DataFrame,
    y_pred: pd.DataFrame,
    k: int,
    user_col: str = 'UserId',
    item_col: str = 'ItemId'
) -> float:
    """
    Calculate Recall@K for recommendations.
    
    Args:
        y_true: DataFrame of ground truth interactions
        y_pred: DataFrame of recommendations
        k: Number of recommendations to consider
        user_col: Name of user ID column
        item_col: Name of item ID column
        
    Returns:
        Recall@K score
    """
    # Group predictions by user and get top k
    user_recs = y_pred.groupby(user_col).head(k)
    
    # Calculate recall for each user
    recalls = []
    for user in y_true[user_col].unique():
        user_true = set(y_true[y_true[user_col] == user][item_col])
        user_pred = set(user_recs[user_recs[user_col] == user][item_col])
        
        if len(user_true) > 0:
            recall = len(user_true.intersection(user_pred)) / len(user_true)
            recalls.append(recall)
            
    return np.mean(recalls) if recalls else 0.0

def ndcg_at_k(
    y_true: pd.DataFrame,
    y_pred: pd.DataFrame,
    k: int,
    user_col: str = 'UserId',
    item_col: str = 'ItemId',
    rating_col: Optional[str] = None
) -> float:
    """
    Calculate NDCG@K for recommendations.
    
    Args:
        y_true: DataFrame of ground truth interactions
        y_pred: DataFrame of recommendations
        k: Number of recommendations to consider
        user_col: Name of user ID column
        item_col: Name of item ID column
        rating_col: Name of rating column (if available)
        
    Returns:
        NDCG@K score
    """
    ndcg_scores = []
    
    for user in y_true[user_col].unique():
        # Get user's true items and predictions
        user_true = y_true[y_true[user_col] == user]
        user_pred = y_pred[y_pred[user_col] == user].head(k)
        
        if len(user_true) == 0 or len(user_pred) == 0:
            continue
            
        # Create relevance array
        relevance = np.zeros(k)
        for i, item in enumerate(user_pred[item_col]):
            if rating_col and item in user_true[item_col].values:
                relevance[i] = user_true[user_true[item_col] == item][rating_col].iloc[0]
            elif item in user_true[item_col].values:
                relevance[i] = 1
                
        # Calculate NDCG
        ideal_relevance = np.sort(relevance)[::-1]
        ndcg = ndcg_score([ideal_relevance], [relevance])
        ndcg_scores.append(ndcg)
        
    return np.mean(ndcg_scores) if ndcg_scores else 0.0

def map_at_k(
    y_true: pd.DataFrame,
    y_pred: pd.DataFrame,
    k: int,
    user_col: str = 'UserId',
    item_col: str = 'ItemId'
) -> float:
    """
    Calculate MAP@K (Mean Average Precision at K) for recommendations.
    
    Args:
        y_true: DataFrame of ground truth interactions
        y_pred: DataFrame of recommendations
        k: Number of recommendations to consider
        user_col: Name of user ID column
        item_col: Name of item ID column
        
    Returns:
        MAP@K score
    """
    ap_scores = []
    
    for user in y_true[user_col].unique():
        # Get user's true items and predictions
        user_true = set(y_true[y_true[user_col] == user][item_col])
        user_pred = y_pred[y_pred[user_col] == user].head(k)[item_col]
        
        if len(user_true) == 0:
            continue
            
        # Calculate precision at each position
        hits = 0
        sum_precs = 0
        
        for i, item in enumerate(user_pred, 1):
            if item in user_true:
                hits += 1
                sum_precs += hits / i
                
        if hits > 0:
            ap_scores.append(sum_precs / min(len(user_true), k))
            
    return np.mean(ap_scores) if ap_scores else 0.0
