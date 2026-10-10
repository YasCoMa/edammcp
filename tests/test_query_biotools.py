"""Tests for the Biotools query functionality."""

import pytest

from edam_mcp.models.query import BiotoolsQueryTextRequest, BiotoolsQueryTermsRequest, BiotoolsQueryResponse, BiotoolsHit
from edam_mcp.tools.query_biotools import query_biotools_by_text, query_biotools_by_edam_terms
from edam_mcp.utils.context import MockContext

class TestQueryBiotools:
    """Test cases for the segment_text async function."""

    @pytest.mark.asyncio
    async def test_query_by_text(self):
        """Test biotools query by text."""

        request = BiotoolsQueryTextRequest(seed="gene regulation", max_results=5)
        context = MockContext()

        result = await query_biotools_by_text(request, context)
        print(result)

        assert isinstance(result, BiotoolsQueryResponse)
        assert isinstance(result.matches[0], BiotoolsHit)

    @pytest.mark.asyncio
    async def test_query_by_terms(self):
        """Test query biotools given a topic and a data type."""

        terms_list = ["http://edamontology.org/topic_3510", "http://edamontology.org/data_1361"] # Respectively: "Protein sites, features and motifs" and "Position frequency matrix"
        request = BiotoolsQueryTermsRequest(edam_terms=terms_list)
        context = MockContext()

        result = await query_biotools_by_edam_terms(request, context)

        assert isinstance(result, BiotoolsQueryResponse)
        assert isinstance(result.matches[0], BiotoolsHit)
        assert len(result.matches) == 10
        