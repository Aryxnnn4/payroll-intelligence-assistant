# Payroll Intelligence Assistant

A secure, role-aware payroll assistant that provides payroll-related information while enforcing privacy, access control, and compliance rules.

## Overview

Payroll Intelligence Assistant is designed to simulate how an enterprise payroll assistant should behave when handling sensitive employee and financial data.  
The system responds differently based on user role and jurisdiction, ensuring privacy, correctness, and compliance at every step.

This project focuses on architecture, safety, and correctness, not on connecting to a real AI model.

## Key Features

- Role-based access control (Employee, HR, Finance)
- Jurisdiction-aware payroll explanations
- Automatic detection and masking of sensitive information
- Privacy-first query handling
- Input sanitization and security checks
- Audit logging for compliance tracking
- Modular and extensible design.

## Architecture
```
payroll_intelligence_assistant/
├── README.md                       # Project overview & architecture
└── src/
    ├── app.py                     # Application entry point & controller
    └── engine/
        ├── prompt_engine.py       # Role-based logic & jurisdiction handling
        └── privacy_guard.py       # Security, PII masking & audit logging
```
  
## Roles Supported

- Employee  
  Can access only their own payroll-related information.

- HR  
  Can handle employee payroll questions and explain policies.

- Finance  
  Can access high-level payroll and compliance information.

## Jurisdictions Supported

- US Federal
- California (US)
- New York (US)
- United Kingdom
- Canada

## Privacy & Security

- Sensitive data such as SSN, bank details, emails, and card numbers are masked
- Unauthorized access attempts are blocked
- Queries are sanitized to prevent misuse
- Role-based data exposure is enforced
- Every interaction is audit-logged

## How It Works

1. User submits a payroll query
2. Role and jurisdiction are validated
3. Input is sanitized
4. Prompt is constructed
5. Response is generated
6. Sensitive data is redacted
7. Audit log is created

## Running the Project
```
python src/app.py --demo
```
## Disclaimer

This project is for educational purposes only and does not provide legal, tax, or financial advice.

## Author

Academic project submission

