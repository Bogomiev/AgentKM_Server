from abc import abstractmethod
from dataclasses import dataclass

from sqlalchemy import and_, or_, not_, true


class Specification:
    @abstractmethod
    def is_satisfied(self):
        raise NotImplementedError()

    def __call__(self):
        return self.is_satisfied()

    def __and__(self, other: "Specification") -> "AndSpecification":
        return AndSpecification(self, other)

    def __or__(self, other: "Specification") -> "OrSpecification":
        return OrSpecification(self, other)

    def __neg__(self) -> "NotSpecification":
        return NotSpecification(self)


@dataclass(frozen=True)
class EmptySpecification(Specification):
    def is_satisfied(self):
        return true


@dataclass(frozen=True)
class AndSpecification(Specification):
    first: Specification
    second: Specification

    def is_satisfied(self):
        return and_(self.first.is_satisfied(), self.second.is_satisfied())


@dataclass(frozen=True)
class OrSpecification(Specification):
    first: Specification
    second: Specification

    def is_satisfied(self):
        return or_(self.first.is_satisfied(), self.second.is_satisfied())


@dataclass(frozen=True)
class NotSpecification(Specification):
    subject: Specification

    def is_satisfied(self):
        return not_(self.subject.is_satisfied())
