# Copyright 2023 Jaedson Silva

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

class InvalidDataError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InvalidMessageError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
