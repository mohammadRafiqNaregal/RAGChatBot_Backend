ROLE_ADMIN = "Admin"
ROLE_HR_USER = "HR User"
ROLE_FINANCE_USER = "Finance User"
ROLE_IT_USER = "IT User"
ROLE_EMPLOYEE = "Employee"

VALID_ROLES = (
    ROLE_ADMIN,
    ROLE_HR_USER,
    ROLE_FINANCE_USER,
    ROLE_IT_USER,
    ROLE_EMPLOYEE,
)

DEPARTMENT_HR = "HR"
DEPARTMENT_FINANCE = "Finance"
DEPARTMENT_IT = "IT"

VALID_DEPARTMENTS = (
    DEPARTMENT_HR,
    DEPARTMENT_FINANCE,
    DEPARTMENT_IT,
)


def normalize_role(value: str) -> str:
    normalized = value.strip()
    if normalized not in VALID_ROLES:
        raise ValueError(f"Role must be one of {list(VALID_ROLES)}")
    return normalized


def normalize_roles(values: list[str]) -> list[str]:
    if not values:
        raise ValueError("allowed_roles must contain at least one valid role")

    normalized_values: list[str] = []
    seen: set[str] = set()
    for value in values:
        normalized = normalize_role(value)
        if normalized not in seen:
            normalized_values.append(normalized)
            seen.add(normalized)
    return normalized_values


def normalize_department(value: str) -> str:
    normalized = value.strip()
    if normalized not in VALID_DEPARTMENTS:
        raise ValueError(f"Department must be one of {list(VALID_DEPARTMENTS)}")
    return normalized


def normalize_optional_department(value: str | None) -> str | None:
    if value is None:
        return None
    return normalize_department(value)