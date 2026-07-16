from fastapi import HTTPException, status


class AuthException:

    @staticmethod
    def invalid_credentials():
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    @staticmethod
    def inactive_user():
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive",
        )

    @staticmethod
    def not_found():
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    @staticmethod
    def invalid_token():
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    @staticmethod
    def forbidden():
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed",
        )

    @staticmethod
    def too_many_requests():
        return HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many failed login attempts. Please try again after 15 minutes.",
        )


class InterviewException:

    @staticmethod
    def not_found():
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found",
        )

    @staticmethod
    def already_started():
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Interview already started",
        )

    @staticmethod
    def already_completed():
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Interview already completed",
        )

    @staticmethod
    def invalid_state():
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Interview is not in a valid state",
        )

    @staticmethod
    def question_not_found():
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found",
        )
