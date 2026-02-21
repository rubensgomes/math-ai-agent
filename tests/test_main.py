import pytest
from httpx import ASGITransport, AsyncClient

from math_ai_agent.main import MathQuestion, app


@pytest.mark.asyncio
async def test_app_is_fastapi_instance():
    assert app.title == "FastAPI"


@pytest.mark.asyncio
async def test_static_files_mount():
    routes = [route.path for route in app.routes]
    assert "/static" in routes or any("/static" in r for r in routes)


@pytest.mark.asyncio
async def test_static_files_not_found():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/static/nonexistent.html")
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_root_returns_html():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        assert "Math AI Agent" in response.text


@pytest.mark.asyncio
async def test_root_contains_form_elements():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/")
        assert "textarea-question-id" in response.text
        assert "button-submit-id" in response.text
        assert "textarea-response-id" in response.text


@pytest.mark.asyncio
async def test_prompt_returns_answer():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/prompt/", json={"question": "What is 2+2?"})
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert data["answer"] == "What is 2+2?"


@pytest.mark.asyncio
async def test_prompt_strips_whitespace():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/prompt/", json={"question": "  hello  "})
        assert response.status_code == 200
        assert response.json()["answer"] == "hello"


@pytest.mark.asyncio
async def test_prompt_missing_question_field():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/prompt/", json={})
        assert response.status_code == 422


@pytest.mark.asyncio
async def test_prompt_invalid_content_type():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/prompt/", content="not json", headers={"content-type": "text/plain"}
        )
        assert response.status_code == 422


@pytest.mark.asyncio
async def test_prompt_empty_body():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/prompt/")
        assert response.status_code == 422


@pytest.mark.asyncio
async def test_prompt_wrong_type_for_question():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/prompt/", json={"question": 123})
        assert response.status_code == 422


@pytest.mark.asyncio
async def test_prompt_get_method_not_allowed():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/prompt/")
        assert response.status_code == 405


def test_math_question_model():
    q = MathQuestion(question="What is 5*3?")
    assert q.question == "What is 5*3?"


def test_math_question_model_requires_question():
    with pytest.raises(Exception):
        MathQuestion()
