from http import HTTPStatus
import httpx
import pytest
import respx
from planet import specs


@pytest.fixture(autouse=True, scope="session")
@respx.mock
def mock_bundles():
    # The following bundles are not real, only used for tests...
    # This force loads the bundles ahead of time so we avoid hitting the API
    # or not mocking the route on first use.
    resp = {
        "bundles": {
            "analytic_udm2": {"assets": {"PSScene": ["ortho_analytic_4b"]}},
            "analytic_3b_udm2": {"assets": {"PSScene": []}},
            "analytic_8b_udm2": {"assets": {"PSScene": []}},
            "analytic_sr": {
                "assets": {"SkySatScene": [], "PSScene": [], "SkySatCollect": []}
            },
            "analytic": {"assets": {"SkySatScene": []}},
            "visual": {"assets": {"PSScene": ["basic_udm2"]}},
        }
    }
    spec_url = "https://api.planet.com/compute/ops/bundles/spec"
    respx.get(spec_url).return_value = httpx.Response(HTTPStatus.OK, json=resp)
    specs.get_bundle_names()
