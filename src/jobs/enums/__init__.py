from enum import Enum


class JobTypes(str, Enum):
    FULL_TIME = "Full-time"
    PART_TIME = "Part-time"
    CONTRACT = "Contract"


class SalaryPeriod(str, Enum):
    ANNUAL = "Annual"
    MONTHLY = "Monthly"

class JobStatus(str, Enum):
    DELETED = "Deleted"
    ACTIVE = "Active"