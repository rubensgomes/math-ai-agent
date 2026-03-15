# General Disclaimer
#
# **AI Generated Content**
#
# This project's source code and documentation were generated predominantly
# by an Artificial Intelligence Large Language Model (AI LLM). The project
# lead, [Rubens Gomes](https://rubensgomes.com), provided initial prompts,
# reviewed, and made refinements to the generated output. While human review and
# refinement have occurred, users should be aware that the output may contain
# inaccuracies, errors, or security vulnerabilities
#
# **Third-Party Content Notice**
#
# This software may include components or snippets derived from third-party
# sources. The software's users and distributors are responsible for ensuring
# compliance with any underlying licenses applicable to such components.
#
# **Copyright Status Statement**
#
# Copyright protection, if any, is limited to the original
# human contributions and modifications made to this project.
# The AI-generated portions of the code and
# documentation are not subject to copyright and are considered to be in the
# public domain.
#
# **Limitation of liability**
#
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES, OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT, OR
# OTHERWISE, ARISING FROM, OUT OF, OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.
#
# **No-Warranty Disclaimer**
#
# THIS SOFTWARE IS PROVIDED 'AS IS,' WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE, AND NONINFRINGEMENT.

"""FastAPI application serving the Math AI Agent web interface.

Exposes a root endpoint (``GET /``) that serves the HTML form and a
``POST /prompt/`` endpoint that accepts a math question and returns
an answer.
"""

import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from math_ai_agent.calc_mcp_client import CalcMCPClient
from math_ai_agent.config import configure_logging
from math_ai_agent.models import MathQuestion

configure_logging()
logger = logging.getLogger(__name__)

STATIC_DIR = Path(__file__).parent / "static"

# -------------------------------------------------
# Create the FastAPI app instance
# -------------------------------------------------
app = FastAPI()
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


# -------------------------------------------------
# Helpers
# -------------------------------------------------
async def get_calcmcp_client() -> CalcMCPClient:
    """Create and connect a CalcMCPClient instance.

    Returns:
        A connected CalcMCPClient ready for tool calls.
    """
    logger.debug("Creating CalcMCPClient instance")
    calcmcp_client = CalcMCPClient()
    await calcmcp_client.__aenter__()
    logger.info("CalcMCPClient connected")
    return calcmcp_client


# ----- Routes -----
@app.get("/", response_class=HTMLResponse)
async def root() -> str:
    """Serve the main HTML page.

    Returns:
        The HTML content of the index page.
    """
    logger.debug("Serving root HTML page")
    return (STATIC_DIR / "index.html").read_text()


@app.post("/prompt/")
async def prompt(payload: MathQuestion) -> dict[str, str]:
    """Accept a math question and return an answer.

    Args:
        payload: The validated math question from the request body.

    Returns:
        A dict containing the ``answer`` key with the response.
    """
    logger.info("Received prompt: %s", payload.question)
    # 1) Connect to MCP server
    calcmcp_client = await get_calcmcp_client()
    # 2) Discover MCP tools
    calcmcp_tools = await calcmcp_client.to_openai_tools()
    # 3) TODO....
    question = payload.question.strip()
    return {"answer": question}
