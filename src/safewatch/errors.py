"""Errors of the facade (tech.md 6.2). The API turns `AppError` into `ApiError` and its status."""

from safewatch.types import JobErrorCode

Detail = str | int | float | None


class AppError(Exception):
    code = "error"
    status = 500

    def __init__(self, message: str, **details: Detail) -> None:
        super().__init__(message)
        self.message = message
        self.details = details


class NotFound(AppError):
    code = "not_found"
    status = 404


class ValidationFailed(AppError):
    code = "validation"
    status = 422


class Conflict(AppError):
    status = 409

    def __init__(self, code: str, message: str, **details: Detail) -> None:
        super().__init__(message, **details)
        self.code = code


class Forbidden(AppError):
    code = "forbidden_role"
    status = 403


class RoleRequired(AppError):
    code = "role_required"
    status = 400


class TooLarge(AppError):
    code = "too_large"
    status = 413


class UnsupportedVideo(AppError):
    code = "unsupported_video"
    status = 415


class FeatureDisabled(AppError):
    """A declared optional feature that is switched off (calculator PDF, contract 2.0.0 К10)."""

    code = "not_implemented"
    status = 501


class InferenceError(Exception):
    """Raised by backends and `RemoteShell`; `run_next_job` turns it into a job status."""

    def __init__(self, code: JobErrorCode, message: str) -> None:
        super().__init__(f"{code}: {message}")
        self.code: JobErrorCode = code
        self.message = message
