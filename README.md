# token_accessor

This package provides a token accessor that can be used to fetch and cache a token from a token provider.

## Notes:
- this is not published to PyPi, so it must be installed via git. As a result, build artifacts are included in this repo
- this is not a public package, so it is not supported for general usage


## Build
This repo contains all of the build artifacts. This is not ideal, but it is the current state of the repo. The build artifacts are included in the repo to make it easier to install the package via git. To build the package, run the following command:

```bash
pipenv run build
```

Be sure to commit + push the updated artifacts to the repo after building.

## Usage

### Installing as a dependency

You can reference this package as you would other python packages.

#### Pipenv

Install package this via:

```
pipenv install git+https://github.com/altis-labs/token_accessor.git#egg=token_accessor
```

### To get a raw token

> **Note**: the `create_<client>_token_accessor` takes in an optional scope.
> Each client has the appropriate defaults set for the scope, so it is not
> required to pass in a scope. Specifying an unsupported/unauthorized scope for
> the client may result in a 404 error

```python
from token_accessor.token_cache_token_accessor import
    create_generic_client_token_accessor

# Create a token accessor
token_accessor = create_generic_client_token_accessor()

# Fetch the token
token = token_accessor.get_token()

# The resulting token can be used directly via:
print(token.token)

# Alternatively, the token has a helper function to get auth HTTP headers
headers = token.get_auth_header()
```

### To use a token for a GraphQL request

```python
from token_accessor.token_cache_token_accessor import
    create_generic_client_token_accessor
from token_accessor.gql_client import GqlClient
from gql import gql

# Create a token accessor
token_accessor = create_generic_client_token_accessor()

query = gql(
    """
        query someGqlQuery(
            $some_variable: String!
        ) {
            someGqlQuery(
                some_variable: $some_variable
            ) {
                some_field
            }
        }
    """)

# Create a gql client with the token accessor, which will automatically fetch and use a token when the request is executed
gql_client = GqlClient("https://someurl.com", token_accessor)

# Execute the GraphQL query
result = gql_client.execute(
    query,
    variable_values={
        "some_variable": "some value"
    }
)
```
