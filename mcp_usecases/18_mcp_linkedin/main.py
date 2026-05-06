

from __future__ import annotations

from mcp.server.fastmcp import FastMCP
import os
import requests
import webbrowser
from urllib.parse import urlencode, quote
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("LinkedIn MCP")

# Environment variables
LINKEDIN_CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID", "").strip()
LINKEDIN_CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET", "").strip()
LINKEDIN_REDIRECT_URI = os.getenv("LINKEDIN_REDIRECT_URI", "").strip()
LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN", "").strip()

# LinkedIn endpoints
AUTH_URL = "https://www.linkedin.com/oauth/v2/authorization"
TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"
PROFILE_URL = "https://api.linkedin.com/v2/userinfo"
UGC_POST_URL = "https://api.linkedin.com/v2/ugcPosts"

# Browser-based fallback posting URL
LINKEDIN_SHARE_BASE_URL = "https://www.linkedin.com/feed/?shareActive=true&text="


def validate_basic_config() -> None:
    """Validate required environment variables for OAuth."""
    missing = []

    if not LINKEDIN_CLIENT_ID:
        missing.append("LINKEDIN_CLIENT_ID")
    if not LINKEDIN_CLIENT_SECRET:
        missing.append("LINKEDIN_CLIENT_SECRET")
    if not LINKEDIN_REDIRECT_URI:
        missing.append("LINKEDIN_REDIRECT_URI")

    if missing:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing)}"
        )


def get_headers() -> dict:
    """Return LinkedIn API headers."""
    if not LINKEDIN_ACCESS_TOKEN:
        raise ValueError("LINKEDIN_ACCESS_TOKEN is missing in .env")

    return {
        "Authorization": f"Bearer {LINKEDIN_ACCESS_TOKEN}",
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def build_auth_url(state: str = "linkedin_mcp_demo") -> str:
    """Build LinkedIn OAuth authorization URL."""
    validate_basic_config()

    params = {
        "response_type": "code",
        "client_id": LINKEDIN_CLIENT_ID,
        "redirect_uri": LINKEDIN_REDIRECT_URI,
        "scope": "openid profile email w_member_social",
        "state": state,
    }
    return f"{AUTH_URL}?{urlencode(params)}"


def exchange_code_for_token(auth_code: str) -> dict:
    """Exchange authorization code for access token."""
    validate_basic_config()

    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": LINKEDIN_REDIRECT_URI,
        "client_id": LINKEDIN_CLIENT_ID,
        "client_secret": LINKEDIN_CLIENT_SECRET,
    }

    response = requests.post(TOKEN_URL, data=data, timeout=60)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        return {
            "error": "Failed to exchange code for token",
            "status_code": response.status_code,
            "response_body": response.text,
        }

    return response.json()


def get_profile_data() -> dict:
    """Fetch current user's LinkedIn profile data."""
    response = requests.get(PROFILE_URL, headers=get_headers(), timeout=60)
    response.raise_for_status()
    return response.json()


def get_person_urn() -> str:
    """
    Fetch current user's LinkedIn Person URN.

    For /v2/userinfo, the user identifier is typically in 'sub'.
    """
    profile = get_profile_data()

    person_id = profile.get("sub") or profile.get("id")
    if not person_id:
        raise ValueError(f"Could not fetch LinkedIn person id. Response: {profile}")

    return f"urn:li:person:{person_id}"


def create_post_text(
    topic: str,
    audience: str = "professionals",
    tone: str = "professional",
    include_hashtags: bool = True,
) -> str:
    """Generate a simple LinkedIn-ready post from a topic."""
    intro_map = {
        "professional": f"Sharing a quick thought on {topic}.",
        "thought-leadership": f"One thing I strongly believe about {topic}:",
        "friendly": f"Here’s something interesting about {topic}.",
        "educational": f"Let’s break down {topic} in a simple way.",
    }

    intro = intro_map.get(tone.lower(), f"Sharing a quick thought on {topic}.")

    body = (
        f"{intro}\n\n"
        f"For {audience}, this matters because it can improve outcomes, "
        f"reduce manual effort, and create more scalable ways of working.\n\n"
        f"Three practical angles to consider:\n"
        f"• Business value and real-world adoption\n"
        f"• Risks, limitations, and governance\n"
        f"• Implementation strategy and measurable impact\n\n"
        f"I’d love to hear how others are approaching this in their teams."
    )

    if include_hashtags:
        tags = topic.lower().replace(",", " ").replace("-", " ").split()
        tags = [f"#{t.capitalize()}" for t in tags[:3] if t.strip()]
        tags.extend(["#LinkedIn", "#Innovation"])
        body = f"{body}\n\n{' '.join(tags)}"

    return body


def build_share_url(text: str) -> str:
    """Build browser-based LinkedIn share URL."""
    return f"{LINKEDIN_SHARE_BASE_URL}{quote(text)}"


@mcp.tool()
def get_linkedin_auth_url() -> dict:
    """
    Get LinkedIn OAuth URL.
    Open it in a browser, approve access, and copy the 'code' from the redirect URL.
    """
    try:
        return {"auth_url": build_auth_url()}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def open_linkedin_auth_url() -> dict:
    """Open LinkedIn OAuth URL in the default browser."""
    try:
        auth_url = build_auth_url()
        webbrowser.open(auth_url)
        return {
            "message": "Opened LinkedIn OAuth URL in browser",
            "auth_url": auth_url,
        }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def save_access_token_from_code(auth_code: str) -> dict:
    """
    Exchange LinkedIn OAuth code for access token.
    Copy the returned access_token into .env as LINKEDIN_ACCESS_TOKEN.
    """
    try:
        return exchange_code_for_token(auth_code)
    except requests.exceptions.Timeout:
        return {"error": "Token exchange request timed out"}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def get_linkedin_profile() -> dict:
    """Fetch current LinkedIn profile information."""
    try:
        return get_profile_data()
    except requests.exceptions.Timeout:
        return {"error": "Profile request timed out"}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def get_linkedin_person_urn() -> dict:
    """Fetch the LinkedIn person URN for the logged-in user."""
    try:
        return {"person_urn": get_person_urn()}
    except requests.exceptions.Timeout:
        return {"error": "Person URN request timed out"}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def generate_linkedin_post(
    topic: str,
    audience: str = "professionals",
    tone: str = "professional",
    include_hashtags: bool = True,
) -> dict:
    """Generate a LinkedIn post from a topic."""
    try:
        post_text = create_post_text(
            topic=topic,
            audience=audience,
            tone=tone,
            include_hashtags=include_hashtags,
        )
        return {
            "topic": topic,
            "generated_post": post_text,
        }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def preview_browser_share_url(text: str) -> dict:
    """Build the browser share URL without opening it."""
    try:
        return {"share_url": build_share_url(text)}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def open_browser_share(text: str) -> dict:
    """Open LinkedIn share composer in the browser with prefilled text."""
    try:
        share_url = build_share_url(text)
        webbrowser.open(share_url)
        return {
            "message": "Opened LinkedIn browser share window",
            "share_url": share_url,
        }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def post_to_linkedin(text: str, visibility: str = "PUBLIC") -> dict:
    """
    Post text directly to LinkedIn using the API.

    visibility: PUBLIC or CONNECTIONS
    """
    try:
        author_urn = get_person_urn()

        payload = {
            "author": author_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": text
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": visibility
            }
        }

        response = requests.post(
            UGC_POST_URL,
            headers=get_headers(),
            json=payload,
            timeout=60,
        )

        return {
            "status_code": response.status_code,
            "response_headers": dict(response.headers),
            "response_body": response.text,
            "author_urn": author_urn,
            "payload": payload,
        }

    except requests.exceptions.Timeout:
        return {
            "error": "Request timed out while posting to LinkedIn",
            "fallback_hint": "Use open_browser_share or generate_and_open_browser_share",
        }
    except requests.exceptions.RequestException as e:
        return {
            "error": str(e),
            "fallback_hint": "Use open_browser_share or generate_and_open_browser_share",
        }
    except Exception as e:
        return {
            "error": str(e),
            "fallback_hint": "Use open_browser_share or generate_and_open_browser_share",
        }


@mcp.tool()
def generate_and_post(
    topic: str,
    audience: str = "professionals",
    tone: str = "professional",
    include_hashtags: bool = True,
    visibility: str = "PUBLIC",
) -> dict:
    """
    Generate a LinkedIn post and try to publish it via API.
    """
    try:
        post_text = create_post_text(
            topic=topic,
            audience=audience,
            tone=tone,
            include_hashtags=include_hashtags,
        )

        result = post_to_linkedin(post_text, visibility)

        return {
            "generated_post": post_text,
            "linkedin_result": result,
        }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def generate_and_open_browser_share(
    topic: str,
    audience: str = "professionals",
    tone: str = "professional",
    include_hashtags: bool = True,
) -> dict:
    """
    Generate a LinkedIn post and open it in browser share mode.
    This is the most reliable fallback if direct API posting fails.
    """
    try:
        post_text = create_post_text(
            topic=topic,
            audience=audience,
            tone=tone,
            include_hashtags=include_hashtags,
        )

        share_url = build_share_url(post_text)
        webbrowser.open(share_url)

        return {
            "generated_post": post_text,
            "share_url": share_url,
            "message": "Opened LinkedIn browser share with generated content",
        }
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    mcp.run()