from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class PromptRequest(BaseModel):
    prompt: str
    expected_keywords: Optional[List[str]] = []
    expected_format: Optional[str] = None
    ideal_length: Optional[int] = 100
    previous_score: Optional[float] = None
    prompt_version: Optional[str] = None

class EvaluationResponse(BaseModel):
    original_prompt: str
    score: float
    metrics: Dict[str, float]
    issues: List[str]
    response_prediction: Dict[str, Any]
    regression_detected: Optional[bool] = False
    previous_score: Optional[float] = None
    score_change: Optional[float] = None
    intent: Optional[str] = None
    template: Optional[str] = None

class Suggestion(BaseModel):
    name: str
    prompt: str
    transformation_steps: List[str]
    domain: Optional[str] = None
    intent: Optional[str] = None
    template: Optional[str] = None

class OptimizationResponse(BaseModel):
    original_prompt: str
    suggestions: List[Suggestion] = []
    improved_prompt: str
    score_before: float
    score_after: float
    metrics_before: Dict[str, float]
    metrics_after: Dict[str, float]

class BehaviorStats(BaseModel):
    verbosity: float
    structure: float
    creativity: float
    safety: float

class ModelResponse(BaseModel):
    model_name: str
    response_text: str
    behavior_stats: BehaviorStats
    behavior_labels: List[str]
    latency_ms: Optional[int] = 0
    source: str = "mock"  # 'real' or 'mock'
    error: Optional[str] = None

class ModelComparisonResponse(BaseModel):
    original_prompt: str
    models: List[ModelResponse]
    explanation: List[str]
    recommendation: Optional[Dict[str, str]] = None

class ApiStatusResponse(BaseModel):
    statuses: Dict[str, str]

class CompareResponse(BaseModel):
    is_malicious: bool
    reason: Optional[str] = None
    responses: Dict[str, str]
    scores: Dict[str, float]
    latency: Dict[str, int]
    best_model: str
    regression_detected: Optional[bool] = False
    previous_score: Optional[float] = None
    score_change: Optional[float] = None


class ABTestRequest(BaseModel):
    prompt_a: str
    prompt_b: str
    expected_keywords: Optional[List[str]] = []
    expected_format: Optional[str] = None
    ideal_length: Optional[int] = 100
    prompt_version: Optional[str] = None


class ABTestResponse(BaseModel):
    prompt_a: str
    prompt_b: str
    metrics_a: Dict[str, float]
    metrics_b: Dict[str, float]
    issues_a: List[str]
    issues_b: List[str]
    score_a: float
    score_b: float
    winner: str
    regression_detected: bool
    message: str


class DatasetEntry(BaseModel):
    prompt: str
    expected_keywords: Optional[List[str]] = []
    expected_format: Optional[str] = None
    ideal_length: Optional[int] = 100
    version: Optional[str] = None


class FeedbackRequest(BaseModel):
    prompt: str
    feedback: str
    score: Optional[float] = None
    comment: Optional[str] = None
