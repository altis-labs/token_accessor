import logging
from typing import Any, Dict, Optional

from gql import Client
from gql.transport.requests import RequestsHTTPTransport
from graphql import DocumentNode

from token_accessor.token_accessor_base import TokenAccessorBase

gql_logger = logging.getLogger("gql.transport.requests")
gql_logger.setLevel(logging.WARNING)


class GqlClient:
    client: Client
    transport: RequestsHTTPTransport
    token_accessor: TokenAccessorBase

    def __init__(
        self,
        url: str,
        token_accessor: TokenAccessorBase,
        fetch_schema_from_transport: Optional[bool] = False,
    ):
        self.token_accessor = token_accessor

        self.transport = RequestsHTTPTransport(url=url)
        self.client = Client(
            transport=self.transport,
            fetch_schema_from_transport=fetch_schema_from_transport,
        )

    def execute(
        self, document: DocumentNode, variable_values: Optional[Dict[str, Any]] = None
    ):
        token = self.token_accessor.get_token()

        self.transport.headers = {**token.get_auth_header()}

        return self.client.execute(document, variable_values)
