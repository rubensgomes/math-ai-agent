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

"""Integration test client for the OpenAI Responses API.

Sends a simple prompt to verify end-to-end connectivity with the
OpenAI API.  Run standalone with::

    poetry run python tests/integration/test_openai_client.py**

** Ensure the LLM defined below is running locally (e.g., ollama run phi)

"""

import logging
import os
import time

from openai import OpenAI

from math_ai_agent.config import configure_logging

configure_logging()
logger = logging.getLogger(__name__)

_SYSTEM_INSTRUCTIONS = "You are a Python expert programmer.\n"

# OpenAI API key stored in my secrets. (NOT FREE)
# _API_KEY = os.environ.get("OPENAI_API_KEY")
# _BASE_URL = "https://api.openai.com/v1"
# _MODEL = "gpt-5.2"

# GitHub Marketplace Model
_API_KEY = os.environ.get("RUBENS_PAT_TOKEN")
_BASE_URL = "https://models.github.ai/inference"
# _MODEL = "openai/gpt-5"
_MODEL = "openai/gpt-4.1"


# Ollama locally running server. Any string works for local Ollama. (FREE)
# _API_KEY = "ollama"
# _BASE_URL = "http://localhost:11434/v1"
# _MODEL = "llama2" # Meta Open-Source 7B size
# _MODEL = "qwen3.5"  # https://ollama.com/library/qwen3.5
# _MODEL = "phi"  # https://ollama.com/library/phi


def run_client() -> None:
    """Connect to LLM and send a prompt."""
    logger.info("Connecting to %s using model %s", _BASE_URL, _MODEL)
    client = OpenAI(
        api_key=_API_KEY,
        base_url=_BASE_URL,
    )

    prompt = "How do I check if a Python object is an instance of a class?"

    logger.debug("========== %s API CALL (BEGIN) ==========", "NEW")
    logger.debug("Sending prompt: %s", prompt)

    try:
        start = time.perf_counter()
        response = client.chat.completions.create(
            model=_MODEL,
            messages=[
                {"role": "system", "content": _SYSTEM_INSTRUCTIONS},
                {"role": "user", "content": prompt},
            ],
        )
        elapsed = time.perf_counter() - start

        logger.info("Response received successfully")
        result = response.choices[0].message.content
        logger.debug("Response text: %s", result)
        print(result)
        print(f"\n[Model: {_MODEL} | API: NEW | " f"Time: {elapsed:.2f}s]\n")
    except Exception:
        logger.exception(
            "Failed to get response from model %s via NEW API",
            _MODEL,
        )
    finally:
        logger.debug("========== %s API CALL (END) ==========", "NEW")


def main() -> None:
    """Entry point for the OpenAI client."""
    run_client()


if __name__ == "__main__":
    main()
