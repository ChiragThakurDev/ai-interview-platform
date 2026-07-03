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
