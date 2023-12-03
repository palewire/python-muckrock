# python-muckrock

A simple Python wrapper for the [MuckRock API](https://www.muckrock.com/api/)

## Getting started

Installation is as easy as:

```bash
pip install python-muckrock
```

## Usage

Import the MuckRock client and initialize it.

```python
from muckrock import MuckRock

client = MuckRock()
```

Request all of the latest FOIA requests.

```python
request_list = client.foia.latest()
```

Request the latest completed FOIA requests.

```python
request_list = client.foia.filter(status="done")
```

Request a particular FOIA request by its identifier.

```python
request = client.foia.get(100)
```

JSON is returned.


## Authentication

To authenticate with the MuckRock API, simply supply your API token when you instantiate the MuckRock client. This will you allow you to do things like access your embargoed requests.

```python
import os
from muckrock import MuckRock

client = MuckRock(token="YOUR TOKEN")
```

Rather than putting your token in your code, consider storing the token in something an environmental variable and using that to authenticate with the API. Anything exported with `MUCKROCK_API_TOKEN` will be automatically used by the client.

### Creating requests

Once you've authenticated, you can create an information request by passing in a title, agency id and document request to the `create` method.

```python
client.foia.create(
    agency_ids=248,
    title="API Test File Request",
    document_request="I would like the government's secret receipe for the world's best burrito.",
)
```

## Other resources

- Code: [github.com/palewire/python-muckrock](https://github.com/palewire/python-muckrock)
- Issues: [github.com/palewire/python-muckrock/issues](https://github.com/palewire/python-muckrock/issues)
- Packaging: [pypi.org/project/python-muckrock](https://pypi.org/project/python-muckrock)
