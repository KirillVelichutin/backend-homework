from fastapi import HTTPException
from typing import Optional, Dict, Any
from enum import Enum


class ErrorCode(Enum):
    TASK_NOT_FOUND = "TASK_NOT_FOUND"
    COMMENT_NOT_FOUND = "COMMENT_NOT_FOUND"
    USER_NOT_FOUND = "USER_NOT_FOUND"
    USER_ALREADY_EXISTS = "USER_ALREADY_EXISTS"
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"

class AppException(HTTPException):
    def __init__(
        self,
        status_code: int,
        error_code: ErrorCode,
        message: str,
        field: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.error_code = error_code.value
        self.message = message
        super().__init__(
            status_code=status_code,
            detail={
                "code": error_code.value,
                "message": message,
                "field": field,
                "details": details or {}
            }
        )

class TaskNotFound(AppException):
    def __init__(self, task_id: int):
        super().__init__(
            status_code=404,
            error_code=ErrorCode.TASK_NOT_FOUND,
            message=f"Задача с идентификатором {task_id} не найдена.",
            details={"task_id": task_id}
        )


class CommentNotFound(AppException):
    def __init__(self, comment_id: int):
        super().__init__(
            status_code=404,
            error_code=ErrorCode.COMMENT_NOT_FOUND,
            message=f"Комментарий с идентификатором {comment_id} не найден.",
            details={"comment_id": comment_id}
        )


class UserNotFoundException(AppException):
    def __init__(self, user_id: int):
        super().__init__(
            status_code=404,
            error_code=ErrorCode.USER_NOT_FOUND,
            message=f"Пользователь с идентификатором {user_id} не найден.",
            details={"user_id": user_id}
        )


TaskNotFoundException = TaskNotFound
