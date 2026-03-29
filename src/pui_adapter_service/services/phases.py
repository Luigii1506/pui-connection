from datetime import date, datetime

from sqlalchemy.orm import Session

from pui_adapter_service.config import Settings
from pui_adapter_service.db.models import AuditLog, OutboundDelivery, PhaseRun, Report, utcnow
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
        phase_1_run = self._start_phase_run(db, report_id=report.id, phase_name="1")
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
        self._complete_phase_run(db, phase_1_run, details={"matches": len(phase_1_matches)})

        requested_from_date, effective_from_date = self._resolve_historical_window(report.payload.get("fecha_desaparicion"))
        phase_2_run = self._start_phase_run(
            db,
            report_id=report.id,
            phase_name="2",
            requested_from_date=requested_from_date,
            effective_from_date=effective_from_date,
        )
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
            payload={
                "requested_from_date": requested_from_date.isoformat() if requested_from_date else None,
                "effective_from_date": effective_from_date.isoformat() if effective_from_date else None,
            },
        )
        phase_2_matches = self._core_search.search_historical_by_curp(
            report.curp,
            from_date=effective_from_date.isoformat() if effective_from_date else None,
        )
        self._notify_matches(db, report, phase_2_matches, phase_busqueda="2")
        report.phase_2_completed_at = utcnow()
        report.updated_at = utcnow()
        self._complete_phase_run(
            db,
            phase_2_run,
            details={
                "matches": len(phase_2_matches),
                "requested_from_date": requested_from_date.isoformat() if requested_from_date else None,
                "effective_from_date": effective_from_date.isoformat() if effective_from_date else None,
            },
        )

        self._add_audit_log(
            db,
            direction="internal",
            event_type="phase-2.completed",
            report_id=report.id,
            payload={"matches": len(phase_2_matches)},
        )

        if self._settings.pui_outbound_enabled:
            response = self._pui_client.finalize_search(report.id)
            self._add_outbound_delivery(
                db,
                report_id=report.id,
                endpoint="busqueda-finalizada",
                phase_busqueda=None,
                delivery_status="sent",
                request_payload={
                    "id": report.id,
                    "institucion_id": self._settings.pui_outbound_institucion_id,
                },
                response_payload=response,
            )
            self._add_audit_log(
                db,
                direction="outbound",
                event_type="busqueda-finalizada.sent",
                report_id=report.id,
                payload=response,
            )
        else:
            self._add_outbound_delivery(
                db,
                report_id=report.id,
                endpoint="busqueda-finalizada",
                phase_busqueda=None,
                delivery_status="skipped",
                request_payload={
                    "id": report.id,
                    "institucion_id": self._settings.pui_outbound_institucion_id,
                },
                response_payload={"reason": "pui_outbound_disabled"},
            )
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
        phase_3_run = self._start_phase_run(db, report_id=report.id, phase_name="3")
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
        self._complete_phase_run(
            db,
            phase_3_run,
            details={"matches": len(phase_3_matches), "since": since},
        )

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
                delivery_status = "sent"
                response_payload = response
            else:
                event_type = "notificar-coincidencia.skipped"
                payload = {
                    "reason": "pui_outbound_disabled",
                    "request": outbound_payload,
                }
                delivery_status = "skipped"
                response_payload = {"reason": "pui_outbound_disabled"}

            self._add_outbound_delivery(
                db,
                report_id=report.id,
                endpoint="notificar-coincidencia",
                phase_busqueda=phase_busqueda,
                delivery_status=delivery_status,
                request_payload=outbound_payload,
                response_payload=response_payload,
            )

            self._add_audit_log(
                db,
                direction="outbound",
                event_type=event_type,
                report_id=report.id,
                payload=payload,
            )

    @staticmethod
    def _start_phase_run(
        db: Session,
        *,
        report_id: str,
        phase_name: str,
        requested_from_date: date | None = None,
        effective_from_date: date | None = None,
    ) -> PhaseRun:
        phase_run = PhaseRun(
            report_id=report_id,
            phase_name=phase_name,
            status="started",
            requested_from_date=requested_from_date,
            effective_from_date=effective_from_date,
        )
        db.add(phase_run)
        return phase_run

    @staticmethod
    def _complete_phase_run(db: Session, phase_run: PhaseRun, *, details: dict) -> None:
        _ = db
        phase_run.status = "completed"
        phase_run.completed_at = utcnow()
        phase_run.details = details

    @staticmethod
    def _add_outbound_delivery(
        db: Session,
        *,
        report_id: str,
        endpoint: str,
        phase_busqueda: str | None,
        delivery_status: str,
        request_payload: dict,
        response_payload: dict,
    ) -> None:
        db.add(
            OutboundDelivery(
                report_id=report_id,
                endpoint=endpoint,
                phase_busqueda=phase_busqueda,
                delivery_status=delivery_status,
                request_payload=request_payload,
                response_payload=response_payload,
            )
        )

    @staticmethod
    def _resolve_historical_window(fecha_desaparicion: str | None) -> tuple[date | None, date | None]:
        if not fecha_desaparicion:
            return None, None

        try:
            requested = datetime.strptime(fecha_desaparicion, "%Y-%m-%d").date()
        except ValueError:
            return None, None

        today = utcnow().date()
        capped = PhaseOrchestrator._subtract_years(today, 12)
        return requested, max(requested, capped)

    @staticmethod
    def _subtract_years(source: date, years: int) -> date:
        try:
            return source.replace(year=source.year - years)
        except ValueError:
            return source.replace(month=2, day=28, year=source.year - years)

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
