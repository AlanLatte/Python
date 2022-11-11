import pydantic
import pyotp

from app.pkg.models.otp import Check2FACommand

__all__ = ["OTPService"]


class OTPService:
    __totp: pyotp.TOTP

    def __init__(self, otp_key: pydantic.SecretStr):
        self.__totp = pyotp.TOTP(otp_key.get_secret_value())

    async def verify_2fa_auth(self, cmd: Check2FACommand) -> bool:
        return self.__totp.verify(cmd.verify_code.get_secret_value())
