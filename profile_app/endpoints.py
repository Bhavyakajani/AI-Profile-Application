from typing import Optional
from profile_app.app import app


@app.get("/profile_query_params")
def index(limit: Optional[int] = 10, has_notes: Optional[bool] = False, sort: Optional[str] = None):
    if has_notes:
        return {"message": f"{limit} Profiles with notes"}
    else:
        return{"data": f"{limit} Profiles without notes"}
@app.get('/profile/stats')
def get_profile_stats():
    return {'data': 'stats for profiles'}
@app.get('/profile/{id}/notes')
def notes_for_profile(id: str):
    return {'data': {'Strong in ServiceNow and Agile', 'Java specialist'}}