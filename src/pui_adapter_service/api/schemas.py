from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


CurpStr = Annotated[str, Field(min_length=18, max_length=18, pattern=r"^[A-Z0-9]{18}$")]
ReportIdStr = Annotated[str, Field(min_length=36, max_length=75)]
BirthPlaceStr = Annotated[str, Field(min_length=0, max_length=20)]
ShortText50 = Annotated[str, Field(min_length=0, max_length=50)]
PhoneStr = Annotated[str, Field(min_length=0, max_length=15)]
EmailStr = Annotated[str, Field(min_length=0, max_length=50)]
Address500 = Annotated[str, Field(min_length=0, max_length=500)]
Number20 = Annotated[str, Field(min_length=0, max_length=20)]
PostalCodeStr = Annotated[str, Field(min_length=0, max_length=5)]
MunicipalityStr = Annotated[str, Field(min_length=0, max_length=100)]
StateStr = Annotated[str, Field(min_length=0, max_length=40)]


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class HealthResponse(StrictModel):
    status: str
    service: str
    environment: str


class LoginRequest(StrictModel):
    usuario: Annotated[str, Field(min_length=3, max_length=3)]
    clave: Annotated[str, Field(min_length=16, max_length=20)]


class LoginResponse(StrictModel):
    token: str


class MessageResponse(StrictModel):
    message: str


class ActivateReportRequest(StrictModel):
    id: ReportIdStr
    curp: CurpStr
    nombre: ShortText50 | None = None
    primer_apellido: ShortText50 | None = None
    segundo_apellido: ShortText50 | None = None
    fecha_nacimiento: Annotated[str, Field(min_length=10, max_length=10)] | None = None
    fecha_desaparicion: Annotated[str, Field(min_length=10, max_length=10)] | None = None
    lugar_nacimiento: BirthPlaceStr
    sexo_asignado: Annotated[str, Field(min_length=1, max_length=1, pattern=r"^[MHX]{1}$")] | None = None
    telefono: PhoneStr | None = None
    correo: EmailStr | None = None
    direccion: Address500 | None = None
    calle: ShortText50 | None = None
    numero: Number20 | None = None
    colonia: ShortText50 | None = None
    codigo_postal: PostalCodeStr | None = None
    municipio_o_alcaldia: MunicipalityStr | None = None
    entidad_federativa: StateStr | None = None


class DeactivateReportRequest(StrictModel):
    id: ReportIdStr
