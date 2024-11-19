from typing import TypedDict, List, Dict

class CorsRule(TypedDict):
    origins: List[str]
    methods: List[str]
    allow_headers: List[str]

CorsOptions = Dict[str, CorsRule]

cors_options: CorsOptions = {
    r"/api/*": {
        "origins": [
            "http://localhost:5173",
            "https://youreview.netlify.app"
        ],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
}
