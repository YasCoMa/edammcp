from fastmcp.server import Context

from ..config import settings
from ..models.query import BiotoolsQueryTextRequest, BiotoolsQueryTermsRequest, BiotoolsQueryResponse
from ..ontology import BiotoolsSearcher

async def query_biotools_by_text(
    request: BiotoolsQueryTextRequest, 
    context: Context,
) -> BiotoolsQueryResponse:
    """Search for tools in Biotools repository.

    This tool takes a textual description as seed and performs a query in the Biotools database. It returns matches
    with name, description, biotools database url, and list of concepts in the four EDAM ontology categories (topic, operation, format and data).

    Args:
        request: Biotools query request containing search seed and parameters.
        context: MCP context for logging and progress reporting.

    Returns:
        Biotools query response with matching tools and their associated EDAM terms.
    """
    context.info(request)
    try:
        # Log the request
        context.info(f"Query keyword: {request.seed[:100]}...")

        searcher = BiotoolsSearcher()
        matches = searcher.query_by_text(
            seed=request.seed,
            max_results=request.max_results,
        )

        context.info(f"Found {len(matches)} tool matches")

        return BiotoolsQueryResponse(
            matches=matches,
            total_matches=len(matches),
        )

    except Exception as e:
        context.error(f"Error in biotools query: {e}")
        raise

async def query_biotools_by_edam_terms(
    request: BiotoolsQueryTermsRequest, 
    context: Context,
) -> BiotoolsQueryResponse:
    """Search for tools in Biotools repository.

    This tool takes a list of EDAM concept URIs and performs a query in the Biotools database. It returns matches
    with name, description, biotools database url, and list of concepts in the four EDAM ontology categories (topic, operation, format and data).

    Args:
        request: Biotools query request containing search seed and parameters.
        context: MCP context for logging and progress reporting.

    Returns:
        Biotools query response with matching tools and their associated EDAM terms.
    """
    context.info(request)
    try:
        # Log the request
        context.info(f"Query keyword: {request.edam_terms[:5]}...")

        searcher = BiotoolsSearcher()
        matches = searcher.query_by_edam_terms(
            edam_terms=request.edam_terms,
            max_results=request.max_results,
        )

        context.info(f"Found {len(matches)} tool matches")

        return BiotoolsQueryResponse(
            matches=matches,
            total_matches=len(matches),
        )

    except Exception as e:
        context.error(f"Error in biotools query: {e}")
        raise