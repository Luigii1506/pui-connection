from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import select

from pui_adapter_service.config import Settings
from pui_adapter_service.db.models import Report
from pui_adapter_service.db.session import get_session_factory
from pui_adapter_service.services.core_adapter import CoreSearchService
from pui_adapter_service.services.phases import PhaseOrchestrator
from pui_adapter_service.services.pui_client import PUIClient


class Phase3SchedulerService:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._session_factory = get_session_factory()
        self._orchestrator = PhaseOrchestrator(
            settings=settings,
            pui_client=PUIClient(settings),
            core_search=CoreSearchService(),
        )

    def run_cycle(self) -> None:
        db = self._session_factory()
        try:
            reports = db.scalars(
                select(Report).where(
                    Report.status == "active",
                    Report.continuous_search_enabled.is_(True),
                )
            ).all()
            for report in reports:
                self._orchestrator.process_continuous_phase(db, report)
        finally:
            db.close()


def create_phase3_scheduler(settings: Settings) -> tuple[BackgroundScheduler, Phase3SchedulerService]:
    service = Phase3SchedulerService(settings)
    scheduler = BackgroundScheduler(timezone="UTC")
    scheduler.add_job(
        service.run_cycle,
        trigger="interval",
        minutes=settings.scheduler_phase3_minutes,
        id="phase_3_cycle",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )
    return scheduler, service
