import numpy as np
from scipy.spatial.distance import jensenshannon

def calculate_tvd(counts1, counts2, shots):
   
    all_outcomes = sorted(set(counts1.keys()) | set(counts2.keys()))
    p = np.array([counts1.get(k, 0) / shots for k in all_outcomes])
    q = np.array([counts2.get(k, 0) / shots for k in all_outcomes])
    return 0.5 * np.sum(np.abs(p - q))

def calculate_js_divergence(counts1, counts2, shots):
    
    all_outcomes = sorted(set(counts1.keys()) | set(counts2.keys()))
    p = np.array([counts1.get(k, 0) / shots for k in all_outcomes])
    q = np.array([counts2.get(k, 0) / shots for k in all_outcomes])
    
    return jensenshannon(p, q, base=2)**2