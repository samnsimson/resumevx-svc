import json
from pydantic_ai import Agent, RunContext
from app.agent.dto import DocumentDependency
from app.agent.models import LLMModel
from app.document.dto import DocumentMetricsOutput
from app.agent.prompts import agent_prompts

document_metrics_agent = Agent[DocumentDependency, DocumentMetricsOutput](
    name="document_metrics_agent",
    model=LLMModel.openai,
    deps_type=DocumentDependency,
    output_type=DocumentMetricsOutput,
    system_prompt=agent_prompts["document_metrics_agent"]["system_prompt"],
    instructions=agent_prompts["document_metrics_agent"]["instructions"],
)


@document_metrics_agent.tool
def latest_resume_details(ctx: RunContext[DocumentDependency]) -> str:
    """Get the latest resume details in structured JSON format. This is the current version of the resume that should be analyzed."""
    data = ctx.deps.session_state.generated_document_data
    if not data: return "No latest resume details found"
    return f"Latest resume details (JSON): {json.dumps(data, indent=2)}"


@document_metrics_agent.tool
def job_requirement(ctx: RunContext[DocumentDependency]) -> str:
    """Get the job requirement/description in text format. This contains the job posting requirements, qualifications, and key responsibilities that should be used to analyze the resume match."""
    description = ctx.deps.session_state.job_description
    if not description: return "No job requirement found"
    return f"Job requirement: {description}"
