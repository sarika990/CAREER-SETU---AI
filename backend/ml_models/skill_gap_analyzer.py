import logging
import torch
from sentence_transformers import SentenceTransformer, util
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class LocalSkillGapAnalyzer:
    def __init__(self):
        # Using a fast, lightweight model for production-like speed
        self.model = SentenceTransformer('paraphrase-MiniLM-L3-v2')

    def analyze(self, user_skills: List[str], target_skills: List[str]) -> Dict[str, Any]:
        if not target_skills:
            return {"matching_skills": [], "missing_skills": [], "readiness_score": 0, "status": "No target skills provided"}
        
        if not user_skills:
            return {
                "matching_skills": [],
                "missing_skills": target_skills,
                "readiness_score": 0,
                "status": "Gap Identified"
            }
            
        # Semantic matching for each target skill
        user_embeddings = self.model.encode(user_skills, convert_to_tensor=True)
        target_embeddings = self.model.encode(target_skills, convert_to_tensor=True)
        
        # Calculate cosine similarity matrix
        cosine_scores = util.cos_sim(target_embeddings, user_embeddings)
        
        matching = []
        missing = []
        scores = []
        
        THRESHOLD = 0.7  # Similarity threshold for a "match"
        
        for i, target_skill in enumerate(target_skills):
            # Find the best match in user skills for this target skill
            best_match_score = torch.max(cosine_scores[i]).item()
            scores.append(best_match_score)
            
            if best_match_score >= THRESHOLD:
                matching.append(target_skill)
            else:
                missing.append(target_skill)
        
        # Readiness score based on average similarity restricted to [0, 100]
        avg_similarity = sum(scores) / len(scores) if scores else 0
        readiness_score = max(0.0, min(100.0, avg_similarity * 100))
        
        return {
            "matching_skills": matching,
            "missing_skills": missing,
            "readiness_score": float(f"{readiness_score:.1f}"),
            "status": "Ready" if readiness_score > 80 else "Improving" if readiness_score > 50 else "Gap Identified"
        }
