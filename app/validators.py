from typing import Callable

from pydantic import Field


class VField(Field):
    def __init__(self, *, validators: list[Callable], **kwargs):
        super().__init__(**kwargs)
        self.validators = validators
        self.t = [self.apply_validators(...)]

    def apply_validators(self, value):
        for validator in self.validators:
            value = validator(value)  # Apply each validator to the value
        return value



