import json
from pydantic_ai import Agent, RunContext
from app.agent.dto import DocumentDependency
from app.agent.models import LLMModel
from app.document.dto import DocumentDataOutput
from app.agent.prompts import agent_prompts

document_rewrite_agent = Agent[DocumentDependency, DocumentDataOutput](
    name="document_rewrite_agent",
    model=LLMModel.rewrite_model,
    deps_type=DocumentDependency,
    output_type=DocumentDataOutput,
    system_prompt=agent_prompts["document_rewrite_agent"]["system_prompt"],
    instructions=agent_prompts["document_rewrite_agent"]["instructions"],
)


@document_rewrite_agent.tool
def latest_resume_details(ctx: RunContext[DocumentDependency]) -> str:
    """Get the latest resume details in structured JSON format. 
    This is the current version of the resume that should be modified based on user instructions."""
    data = ctx.deps.session_state.generated_document_data
    if not data: return "No latest resume details found"
    return f"Latest resume details in structured JSON format: {json.dumps(data, indent=2)}"


@document_rewrite_agent.tool
def original_resume_details(ctx: RunContext[DocumentDependency]) -> str:
    """Get the original resume details in structured JSON format. 
    This is the initial version of the resume that was extracted from the uploaded document."""
    data = ctx.deps.session_state.document_data
    if not data: return "No original resume details found"
    return f"Original resume details in structured JSON format: {json.dumps(data, indent=2)}"


@document_rewrite_agent.tool
def job_requirement(ctx: RunContext[DocumentDependency]) -> str:
    """Get the job requirement/description in text format. 
    This contains the job posting requirements, qualifications, and key responsibilities that should be used to optimize the resume."""
    description = ctx.deps.session_state.job_description
    if not description: return "No job requirement found"
    return f"Job requirement: {description}"


@document_rewrite_agent.tool
def message_history(ctx: RunContext[DocumentDependency]) -> str:
    """Get the message history in structured JSON format. 
    This contains the message history of the conversation between the user and the assistant."""
    history = ctx.deps.message_history
    if not history: return "No message history found"
    history_dicts = [msg.model_dump() if hasattr(msg, 'model_dump') else msg for msg in history]
    return f"Message history in structured JSON format: {json.dumps(history_dicts, indent=2, default=str)}"
