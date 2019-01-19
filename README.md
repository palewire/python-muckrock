# python-muckrock

A simple python wrapper for the [MuckRock API](https://www.muckrock.com/api/)

Still very much experimental and incomplete.


### Getting started

Installation is as easy as:

```bash
$ pip install python-muckrock
```


### Usage

Import the MuckRock client and initialize it.

```python
>>> from muckrock import MuckRock
>>> client = MuckRock()
```

Request all of the latest FOIA requests.

```python
>>> request_list = client.foia.get()
```

Request the latest completed FOIA requests.

```python
>>> request_list = client.foia.get(status="done")
```

JSON is returned.


### Yet to come.

Almost everything. This library does not now support anything beyond simple FOIA list requests. It cannot authenticate users. Nor can it create new requests. The API does support those features and I hope to gradually add them. 
