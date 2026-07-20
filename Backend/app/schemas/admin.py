from datetime import datetime

from pydantic import BaseModel


class AdminDashboardResponse(BaseModel):

    total_users: int

    active_users: int

    inactive_users: int

    total_interviews: int

    completed_interviews: int

    pending_interviews: int

    total_reports: int

    average_score: float


class AdminUserResponse(BaseModel):

    id: int

    name: str

    email: str

    role: str

    is_active: bool

    created_at: datetime

    class Config:
        from_attributes = True


class RecentUserResponse(BaseModel):

    id: int

    name: str

    email: str

    created_at: datetime

    class Config:
        from_attributes = True


class RecentInterviewResponse(BaseModel):

    id: int

    role: str

    difficulty: str

    status: str

    created_at: datetime

    class Config:
        from_attributes = True


class RecentReportResponse(BaseModel):

    id: int

    interview_id: int

    overall_score: int

    created_at: datetime

    class Config:
        from_attributes = True


class RecentActivityResponse(BaseModel):

    recent_users: list[RecentUserResponse]

    recent_interviews: list[RecentInterviewResponse]

    recent_reports: list[RecentReportResponse]

class PaginatedUsersResponse(BaseModel):

    page: int

    limit: int

    total: int

    users: list[AdminUserResponse]

