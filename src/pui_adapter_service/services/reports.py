import hashlib
import json

from sqlalchemy import select
from sqlalchemy.orm import Session

from pui_adapter_service.db.models import AuditLog, InboundEvent, Report, utcnow


def _payload_hash(payload: dict) -> str:
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _add_audit_log(
    db: Session,
    *,
    direction: str,
    event_type: str,
    report_id: str | None,
    payload: dict,
) -> None:
    db.add(
        AuditLog(
            direction=direction,
            event_type=event_type,
            report_id=report_id,
            payload=payload,
        )
    )


def activate_report(db: Session, *, event_type: str, payload: dict, is_test: bool) -> bool:
    report_id = payload["id"]
    payload_hash = _payload_hash(payload)
    existing = db.scalar(
        select(InboundEvent).where(
            InboundEvent.event_type == event_type,
            InboundEvent.report_id == report_id,
            InboundEvent.payload_hash == payload_hash,
        )
    )
    if existing is not None:
        _add_audit_log(
            db,
            direction="inbound",
            event_type=f"{event_type}.duplicate",
            report_id=report_id,
            payload={"idempotent": True, "payload": payload},
        )
        db.commit()
        return True

    report = db.get(Report, report_id)
    if report is None:
        report = Report(
            id=report_id,
            curp=payload["curp"],
            status="active",
            is_test=is_test,
            continuous_search_enabled=True,
            payload=payload,
        )
        db.add(report)
    else:
        report.curp = payload["curp"]
        report.status = "active"
        report.is_test = is_test
        report.continuous_search_enabled = True
        report.payload = payload
        report.updated_at = utcnow()

    db.add(
        InboundEvent(
            event_type=event_type,
            report_id=report_id,
            payload_hash=payload_hash,
            payload=payload,
        )
    )
    _add_audit_log(
        db,
        direction="inbound",
        event_type=event_type,
        report_id=report_id,
        payload=payload,
    )
    db.commit()
    return False


def deactivate_report(db: Session, *, payload: dict) -> bool:
    report_id = payload["id"]
    payload_hash = _payload_hash(payload)
    existing = db.scalar(
        select(InboundEvent).where(
            InboundEvent.event_type == "desactivar-reporte",
            InboundEvent.report_id == report_id,
            InboundEvent.payload_hash == payload_hash,
        )
    )
    if existing is not None:
        _add_audit_log(
            db,
            direction="inbound",
            event_type="desactivar-reporte.duplicate",
            report_id=report_id,
            payload={"idempotent": True, "payload": payload},
        )
        db.commit()
        return True

    report = db.get(Report, report_id)
    if report is not None:
        report.status = "inactive"
        report.continuous_search_enabled = False
        report.updated_at = utcnow()

    db.add(
        InboundEvent(
            event_type="desactivar-reporte",
            report_id=report_id,
            payload_hash=payload_hash,
            payload=payload,
        )
    )
    _add_audit_log(
        db,
        direction="inbound",
        event_type="desactivar-reporte",
        report_id=report_id,
        payload=payload,
    )
    db.commit()
    return False
