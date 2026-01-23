import json
from pydantic_ai import Agent, RunContext
from app.agent.dto import DocumentDependency
from app.agent.models import LLMModel
from app.document.dto import CoverLetter
from app.agent.prompts import agent_prompts

cover_letter_agent = Agent[DocumentDependency, CoverLetter](
    name="cover_letter_agent",
    model=LLMModel.rewrite_model,
    deps_type=DocumentDependency,
    output_type=CoverLetter,
    system_prompt=agent_prompts["cover_letter_agent"]["system_prompt"],
    instructions=agent_prompts["cover_letter_agent"]["instructions"],
)


@cover_letter_agent.tool
def latest_resume_details(ctx: RunContext[DocumentDependency]) -> str:
    """Get the latest resume details in structured JSON format. 
    This is the current version of the resume that should be used to create the cover letter."""
    data = ctx.deps.session_state.generated_document_data
    if not data: return "No latest resume details found"
    return f"Latest resume details in structured JSON format: {json.dumps(data, indent=2)}"


@cover_letter_agent.tool
def original_resume_details(ctx: RunContext[DocumentDependency]) -> str:
    """Get the original resume details in structured JSON format. 
    This is the initial version of the resume that was extracted from the uploaded document."""
    data = ctx.deps.session_state.document_data
    if not data: return "No original resume details found"
    return f"Original resume details in structured JSON format: {json.dumps(data, indent=2)}"


@cover_letter_agent.tool
def job_requirement(ctx: RunContext[DocumentDependency]) -> str:
    """Get the job requirement/description in text format. 
    This contains the job posting requirements, qualifications, and key responsibilities that should be used to tailor the cover letter."""
    description = ctx.deps.session_state.job_description
    if not description: return "No job requirement found"
    return f"Job requirement: {description}"
