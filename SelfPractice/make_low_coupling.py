# https://www.youtube.com/watch?v=qR4-PBLUZNw&list=PLC0nd42SBTaNuP4iB4L6SJlMaHE71FG6N&index=3
# https://github.com/ArjanCodes/2022-coupling

# Tip 1: Avoid deep inheritance relationships : 상속하기 보다는 사용하기
# Tip 2: Separate creating resources from using them : 생성과 사용을 분리하기
# Tip 3: Introduce abstractions : 추상화 하기
# Tip 4: Avoid inappropriate intimacy: 불필요한 데이터 넘기기 않기
# Tip 5: Introduce an intermediate data structur : 중간 단계의 데이터 구조를 만들어라


from typing import Protocol
from dataclasses import dataclass, field


class EmailServer(Protocol):
    @property
    def _host(self) -> str:
        ...

    def connect(self, host: str, port: int) -> None:
        ...

    def send_email(self, from_address: str, to_address: str, message: str) -> None:
        ...


@dataclass
class Geolocation:
    ...


@dataclass
class Location:
    geolocation: list[Geolocation] = field(default_factory=list)


# def generate_breadcrumbs(localtion: Location) -> dict[str, str]:
def generate_breadcrumbs(geolocation: Geolocation) -> dict[str, str]:
    ...
