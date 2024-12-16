from abc import ABC, abstractmethod


class OTPSender(ABC):
    @abstractmethod
    def send_otp(self, recipient: str, otp: str) -> None:
        pass
