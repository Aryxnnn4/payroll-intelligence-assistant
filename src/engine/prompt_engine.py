"""
Prompt Engine
Responsible for role-aware and region-aware prompt generation
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict
import re


class Role(Enum):
    EMPLOYEE = "employee"
    HR = "hr"
    FINANCE = "finance"


class Region(Enum):
    US_FEDERAL = "us_federal"
    US_CALIFORNIA = "us_california"
    US_NEW_YORK = "us_new_york"
    UK = "uk"
    CANADA = "canada"


@dataclass
class UserProfile:
    role: Role
    region: Region
    user_id: str
    clearance: int


class PromptEngine:
    def __init__(self):
        self.rules = {
            Role.EMPLOYEE: ["own_pay"],
            Role.HR: ["employee_pay", "policy"],
            Role.FINANCE: ["all_pay", "reports"]
        }

    def compose_prompt(self, profile: UserProfile, query: str) -> str:
        return f"""
SYSTEM ROLE: Payroll Assistant
USER ROLE: {profile.role.value}
REGION: {profile.region.value}
CLEARANCE LEVEL: {profile.clearance}

GUIDELINES:
- Respect role permissions
- Follow regional payroll standards
- Do not expose private data
- Provide clear explanations only

USER QUESTION:
{query}
"""

    def check_permissions(self, profile: UserProfile, query: str) -> Dict:
        if profile.role == Role.EMPLOYEE:
            if re.search(r"other employee|coworker|someone else", query.lower()):
                return {
                    "allowed": False,
                    "reason": "Employees may not access other employees' payroll data."
                }
        return {"allowed": True}
