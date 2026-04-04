"""Content report endpoints (Task 048)."""

from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..database import get_db
from ..dependencies import get_current_user_id
from ..models import ContentReport, Story, Word
from ..schemas import (
    REPORT_CATEGORIES,
    REPORT_CONTENT_TYPES,
    REPORT_STATUSES,
    ContentReportCreateRequest,
    ContentReportListResponse,
    ContentReportResponse,
    ContentReportUpdateRequest,
)

router = APIRouter(prefix="/api/reports")

RATE_LIMIT_MAX = 10
RATE_LIMIT_WINDOW_HOURS = 1


def _to_response(report: ContentReport) -> ContentReportResponse:
    return ContentReportResponse(
        id=report.id,
        userId=report.user_id,
        contentType=report.content_type,
        contentId=report.content_id,
        category=report.category,
        description=report.description,
        status=report.status,
        resolutionNote=report.resolution_note,
        createdAt=report.created_at.isoformat() if report.created_at else "",
        updatedAt=report.updated_at.isoformat() if report.updated_at else "",
    )


@router.post("", status_code=status.HTTP_201_CREATED, response_model=ContentReportResponse)
def create_report(
    body: ContentReportCreateRequest,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> ContentReportResponse:
    # Validate content_type
    if body.contentType not in REPORT_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"content_type must be one of: {', '.join(sorted(REPORT_CONTENT_TYPES))}",
        )

    # Validate category
    if body.category not in REPORT_CATEGORIES:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"category must be one of: {', '.join(sorted(REPORT_CATEGORIES))}",
        )

    # Validate content_id exists
    if body.contentType == "story":
        exists = db.query(Story).filter(Story.id == body.contentId).first()
    else:
        exists = db.query(Word).filter(Word.id == body.contentId).first()

    if not exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{body.contentType} with id '{body.contentId}' not found",
        )

    # Check for duplicate active report from same user
    duplicate = (
        db.query(ContentReport)
        .filter(
            ContentReport.user_id == user_id,
            ContentReport.content_type == body.contentType,
            ContentReport.content_id == body.contentId,
            ContentReport.status == "new",
        )
        .first()
    )
    if duplicate:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You already have an active report for this item",
        )

    # Rate limit: max 10 reports per user per hour
    window_start = datetime.now(timezone.utc) - timedelta(hours=RATE_LIMIT_WINDOW_HOURS)
    recent_count = (
        db.query(func.count(ContentReport.id))
        .filter(
            ContentReport.user_id == user_id,
            ContentReport.created_at >= window_start,
        )
        .scalar()
    )
    if recent_count is not None and recent_count >= RATE_LIMIT_MAX:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Maximum 10 reports per hour.",
        )

    report = ContentReport(
        user_id=user_id,
        content_type=body.contentType,
        content_id=body.contentId,
        category=body.category,
        description=body.description,
        status="new",
    )
    db.add(report)
    db.commit()
    db.refresh(report)

    return _to_response(report)


@router.get("", response_model=ContentReportListResponse)
def list_reports(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
    report_status: str | None = Query(default=None, alias="status"),
    content_type: str | None = Query(default=None),
    category: str | None = Query(default=None),
    language: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> ContentReportListResponse:
    query = db.query(ContentReport)

    if report_status:
        query = query.filter(ContentReport.status == report_status)
    if content_type:
        query = query.filter(ContentReport.content_type == content_type)
    if category:
        query = query.filter(ContentReport.category == category)

    # Language filter: join to Story or Word to check the language field
    if language:
        story_ids = db.query(Story.id).filter(Story.language == language).subquery()
        word_ids = db.query(Word.id).filter(Word.language == language).subquery()
        query = query.filter(
            (
                (ContentReport.content_type == "story")
                & ContentReport.content_id.in_(story_ids)
            )
            | (
                (ContentReport.content_type == "word")
                & ContentReport.content_id.in_(word_ids)
            )
        )

    total = query.count()
    reports = query.order_by(ContentReport.created_at.desc()).offset(offset).limit(limit).all()

    return ContentReportListResponse(
        items=[_to_response(r) for r in reports],
        total=total,
    )


@router.patch("/{report_id}", response_model=ContentReportResponse)
def update_report(
    report_id: str,
    body: ContentReportUpdateRequest,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> ContentReportResponse:
    if body.status not in REPORT_STATUSES:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"status must be one of: {', '.join(sorted(REPORT_STATUSES))}",
        )

    report = db.query(ContentReport).filter(ContentReport.id == report_id).first()
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found",
        )

    report.status = body.status
    if body.resolutionNote is not None:
        report.resolution_note = body.resolutionNote

    db.commit()
    db.refresh(report)

    return _to_response(report)
