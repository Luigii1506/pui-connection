from sqlalchemy.orm import Session

from pui_adapter_service.config import Settings
from pui_adapter_service.db.models import AuditLog, Report, utcnow
from pui_adapter_service.services.core_adapter import CoreSearchService
from pui_adapter_service.services.pui_client import PUIClient


class PhaseOrchestrator:
    def __init__(
        self,
        *,
        settings: Settings,
        pui_client: PUIClient,
        core_search: CoreSearchService,
    ) -> None:
        self._settings = settings
        self._pui_client = pui_client
        self._core_search = core_search

    def process_initial_phases(self, db: Session, report: Report) -> None:
        self._add_audit_log(
            db,
            direction="internal",
            event_type="phase-1.started",
            report_id=report.id,
            payload={"curp": report.curp},
        )
        phase_1_matches = self._core_search.search_basic_by_curp(report.curp)
        self._notify_matches(db, report, phase_1_matches, phase_busqueda="1")
        report.phase_1_completed_at = utcnow()

        self._add_audit_log(
            db,
            direction="internal",
            event_type="phase-1.completed",
            report_id=report.id,
            payload={"matches": len(phase_1_matches)},
        )

        self._add_audit_log(
            db,
            direction="internal",
            event_type="phase-2.started",
            report_id=report.id,
            payload={"from_date": report.payload.get("fecha_desaparicion")},
        )
        phase_2_matches = self._core_search.search_historical_by_curp(
            report.curp,
            from_date=report.payload.get("fecha_desaparicion"),
        )
        self._notify_matches(db, report, phase_2_matches, phase_busqueda="2")
        report.phase_2_completed_at = utcnow()
        report.updated_at = utcnow()

        self._add_audit_log(
            db,
            direction="internal",
            event_type="phase-2.completed",
            report_id=report.id,
            payload={"matches": len(phase_2_matches)},
        )

        if self._settings.pui_outbound_enabled:
            response = self._pui_client.finalize_search(report.id)
            self._add_audit_log(
                db,
                direction="outbound",
                event_type="busqueda-finalizada.sent",
                report_id=report.id,
                payload=response,
            )
        else:
            self._add_audit_log(
                db,
                direction="outbound",
                event_type="busqueda-finalizada.skipped",
                report_id=report.id,
                payload={"reason": "pui_outbound_disabled"},
            )

        db.commit()

    def process_continuous_phase(self, db: Session, report: Report) -> None:
        if report.status != "active" or not report.continuous_search_enabled:
            return

        since = report.last_phase_3_check_at.isoformat() if report.last_phase_3_check_at else None
        self._add_audit_log(
            db,
            direction="internal",
            event_type="phase-3.started",
            report_id=report.id,
            payload={"since": since},
        )

        phase_3_matches = self._core_search.search_continuous_by_curp(report.curp, since=since)
        self._notify_matches(db, report, phase_3_matches, phase_busqueda="3")
        report.last_phase_3_check_at = utcnow()
        report.updated_at = utcnow()

        self._add_audit_log(
            db,
            direction="internal",
            event_type="phase-3.completed",
            report_id=report.id,
            payload={"matches": len(phase_3_matches)},
        )
        db.commit()

    def _notify_matches(
        self,
        db: Session,
        report: Report,
        matches: list[dict],
        *,
        phase_busqueda: str,
    ) -> None:
        for match in matches:
            outbound_payload = {
                "curp": report.curp,
                "id": report.id,
                "institucion_id": self._settings.pui_outbound_institucion_id,
                "lugar_nacimiento": report.payload["lugar_nacimiento"],
                "fase_busqueda": phase_busqueda,
                **match,
            }
            if self._settings.pui_outbound_enabled:
                response = self._pui_client.notify_coincidence(outbound_payload)
                event_type = "notificar-coincidencia.sent"
                payload = {"request": outbound_payload, "response": response}
            else:
                event_type = "notificar-coincidencia.skipped"
                payload = {
                    "reason": "pui_outbound_disabled",
                    "request": outbound_payload,
                }

            self._add_audit_log(
                db,
                direction="outbound",
                event_type=event_type,
                report_id=report.id,
                payload=payload,
            )

    @staticmethod
    def _add_audit_log(
        db: Session,
        *,
        direction: str,
        event_type: str,
        report_id: str,
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
