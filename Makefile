generate:
ifdef message
	alembic revision --autogenerate -m "$(message)"
else
	@read -p "Enter migration message: " msg && alembic revision --autogenerate -m "$$msg"
endif

migrate:
	alembic upgrade head

rollback:
	alembic downgrade -1

models:
	@echo "Fetching OpenAPI spec from http://localhost:8888/api/docs/openapi..."
	@curl -s http://localhost:8888/api/docs/openapi -o authapi.json || (echo "Error: Failed to fetch OpenAPI spec. Make sure the better-auth server is running on localhost:8888" && exit 1)
	@echo "Generating models from authapi.json..."
	@datamodel-codegen --input authapi.json --output app/auth/model.py --output-model-type pydantic_v2.BaseModel --class-name-prefix Auth
	@echo "Models generated successfully!"