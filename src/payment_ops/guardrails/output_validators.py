"""
Output Guardrails for Payment Operations Agent
Implements OpenAI Agent SDK output guardrail patterns using @output_guardrail decorator
"""

from pydantic import BaseModel
from agents import (
    Agent,
    GuardrailFunctionOutput,
    RunContextWrapper,
    Runner,
    output_guardrail,
)


class ComplianceValidationOutput(BaseModel):
    """Output model for compliance response validation"""
    meets_compliance_standards: bool
    reasoning: str
    missing_disclaimers: list[str] = []
    risk_assessment_complete: bool = False
    contains_sensitive_data: bool = False


class CustomerServiceValidationOutput(BaseModel):
    """Output model for customer service response validation"""
    appropriate_tone: bool
    reasoning: str
    tone_issues: list[str] = []
    contains_sensitive_data: bool = False
    professional_language: bool = True


# Compliance output validation agent
compliance_validation_agent = Agent(
    name="ComplianceOutputValidator",
    instructions="""You are a compliance output validation agent. Analyze agent responses for:

1. Legal disclaimers and risk assessments
2. Compliance with regulatory requirements
3. Sensitive data exposure prevention
4. Professional compliance language

Compliance standards require:
- Risk assessments for high-value transactions
- Legal disclaimers for regulatory matters
- No exposure of confidential information
- Professional language appropriate for compliance

Return validation results with specific compliance issues if any.""",
    output_type=ComplianceValidationOutput,
)


# Customer service output validation agent
customer_service_validation_agent = Agent(
    name="CustomerServiceOutputValidator",
    instructions="""You are a customer service output validation agent. Analyze agent responses for:

1. Appropriate tone and language
2. Professional customer communication standards
3. Sensitive data exposure prevention
4. Helpful and respectful content

Customer service standards require:
- Professional, helpful tone
- Clear, understandable language
- No exposure of sensitive customer information
- Appropriate responses to customer concerns

Return validation results with specific tone or content issues if any.""",
    output_type=CustomerServiceValidationOutput,
)


@output_guardrail
async def validate_compliance_response(
    ctx: RunContextWrapper[None],
    agent: Agent,
    output: str
) -> GuardrailFunctionOutput:
    """
    SDK-native output guardrail for compliance response validation

    Args:
        ctx: Run context wrapper
        agent: Agent that generated the output
        output: Agent output to validate

    Returns:
        GuardrailFunctionOutput with compliance validation results
    """
    # Run compliance validation using guardrail agent
    result = await Runner.run(
        compliance_validation_agent,
        f"Validate this compliance response: {output}",
        context=ctx.context
    )

    compliance_output = result.final_output_as(ComplianceValidationOutput)

    # Trigger tripwire if compliance standards are not met
    tripwire_triggered = not compliance_output.meets_compliance_standards

    return GuardrailFunctionOutput(
        output_info=compliance_output,
        tripwire_triggered=tripwire_triggered,
    )


@output_guardrail
async def validate_customer_service_response(
    ctx: RunContextWrapper[None],
    agent: Agent,
    output: str
) -> GuardrailFunctionOutput:
    """
    SDK-native output guardrail for customer service response validation

    Args:
        ctx: Run context wrapper
        agent: Agent that generated the output
        output: Agent output to validate

    Returns:
        GuardrailFunctionOutput with customer service validation results
    """
    # Run customer service validation using guardrail agent
    result = await Runner.run(
        customer_service_validation_agent,
        f"Validate this customer service response: {output}",
        context=ctx.context
    )

    service_output = result.final_output_as(CustomerServiceValidationOutput)

    # Trigger tripwire if standards are not met
    tripwire_triggered = (
        not service_output.appropriate_tone
        or not service_output.professional_language
    )

    return GuardrailFunctionOutput(
        output_info=service_output,
        tripwire_triggered=tripwire_triggered,
    )


# General sensitive data screening guardrail
class SensitiveDataOutput(BaseModel):
    """Output model for sensitive data screening"""
    contains_sensitive_data: bool
    reasoning: str
    detected_data_types: list[str] = []
    sanitization_required: bool = False


sensitive_data_agent = Agent(
    name="SensitiveDataValidator",
    instructions="""You are a sensitive data screening agent. Analyze agent responses for:

1. Personal identifiable information (PII)
2. Financial data (account numbers, card details)
3. Confidential business information
4. Authentication credentials

Sensitive data types to detect:
- Credit card numbers or partial card numbers
- Social security numbers
- Account numbers
- Authentication tokens or passwords
- Customer personal information

Return validation results with specific data types detected if any.""",
    output_type=SensitiveDataOutput,
)


@output_guardrail
async def validate_sensitive_data_screening(
    ctx: RunContextWrapper[None],
    agent: Agent,
    output: str
) -> GuardrailFunctionOutput:
    """
    SDK-native output guardrail for sensitive data screening

    Args:
        ctx: Run context wrapper
        agent: Agent that generated the output
        output: Agent output to validate

    Returns:
        GuardrailFunctionOutput with sensitive data validation results
    """
    # Run sensitive data screening using guardrail agent
    result = await Runner.run(
        sensitive_data_agent,
        f"Screen this response for sensitive data: {output}",
        context=ctx.context
    )

    sensitive_output = result.final_output_as(SensitiveDataOutput)

    # Trigger tripwire if sensitive data is detected
    tripwire_triggered = sensitive_output.contains_sensitive_data

    return GuardrailFunctionOutput(
        output_info=sensitive_output,
        tripwire_triggered=tripwire_triggered,
    )
