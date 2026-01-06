"""
Payroll Intelligence Assistant
Main application controller
"""

import sys
import os
import logging
from dataclasses import dataclass
from typing import Dict, Any, Optional

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from engine.prompt_engine import PromptEngine, UserProfile, Role, Region
from engine.privacy_guard import PrivacyGuard

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger("PayrollApp")


@dataclass
class PayrollRequest:
    user_id: str
    role: str
    region: str
    message: str
    metadata: Optional[Dict[str, Any]] = None


class PayrollAssistant:
    def __init__(self):
        self.prompt_engine = PromptEngine()
        self.privacy_guard = PrivacyGuard()
        logger.info("Payroll Assistant ready")

    def handle_request(self, request: PayrollRequest) -> Dict[str, Any]:
        try:
            user_profile = self._build_user_profile(request)
            clean_query = self.privacy_guard.clean_input(request.message)

            permission = self.prompt_engine.check_permissions(user_profile, clean_query)
            if not permission["allowed"]:
                return self._deny(permission)

            violations = self.privacy_guard.scan_query(clean_query, user_profile.__dict__)
            if violations:
                return self._block(violations)

            prompt = self.prompt_engine.compose_prompt(user_profile, clean_query)
            raw_response = self._mock_ai_response(prompt, user_profile)

            safe_response, redactions = self.privacy_guard.mask_sensitive_data(
                raw_response, user_profile.role.value
            )

            audit = self.privacy_guard.log_event(
                user_profile.__dict__,
                clean_query,
                safe_response,
                redactions
            )

            final_output = self.privacy_guard.apply_disclaimers(
                safe_response, user_profile.__dict__
            )

            return {
                "success": True,
                "response": final_output,
                "meta": {
                    "role": user_profile.role.value,
                    "region": user_profile.region.value,
                    "redactions": len(redactions),
                    "timestamp": audit["timestamp"]
                }
            }

        except Exception as exc:
            logger.error(str(exc))
            return self._error()

    def _build_user_profile(self, request: PayrollRequest) -> UserProfile:
        role_map = {
            "employee": Role.EMPLOYEE,
            "hr": Role.HR,
            "finance": Role.FINANCE
        }
        region_map = {
            "us_federal": Region.US_FEDERAL,
            "us_california": Region.US_CALIFORNIA,
            "us_new_york": Region.US_NEW_YORK,
            "uk": Region.UK,
            "canada": Region.CANADA
        }

        return UserProfile(
            role=role_map.get(request.role.lower(), Role.EMPLOYEE),
            region=region_map.get(request.region.lower(), Region.US_FEDERAL),
            user_id=request.user_id,
            clearance={"employee": 1, "hr": 2, "finance": 3}[request.role.lower()]
        )

    def _mock_ai_response(self, prompt: str, profile: UserProfile) -> str:
        text = prompt.lower()
        if "overtime" in text:
            return "Overtime pay depends on hours worked beyond standard limits."
        if "tax" in text:
            return "Tax withholdings are calculated using government guidelines."
        if "benefit" in text:
            return "Benefits are deducted based on enrollment selections."
        return "Payroll information is processed according to company policy."

    def _deny(self, info: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "success": False,
            "error": "ACCESS_DENIED",
            "response": info["reason"]
        }

    def _block(self, violations: list) -> Dict[str, Any]:
        return {
            "success": False,
            "error": "PRIVACY_BLOCK",
            "response": "Request cannot be processed due to privacy constraints."
        }

    def _error(self) -> Dict[str, Any]:
        return {
            "success": False,
            "error": "SYSTEM_FAILURE",
            "response": "An unexpected error occurred."
        }


def main():
    assistant = PayrollAssistant()

    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        demo = PayrollRequest(
            user_id="EMP100",
            role="employee",
            region="us_california",
            message="How is my overtime calculated?"
        )
        result = assistant.handle_request(demo)
        print(result["response"])
    else:
        print("Payroll Assistant initialized")


if __name__ == "__main__":
    main()
