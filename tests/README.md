# Running tests

<!-- mdformat-toc start --slug=github --maxlevel=6 --minlevel=2 -->

- [Installing dependencies](#installing-dependencies)
- [Executing tests](#executing-tests)
- [Running live tests & updating mocks](#running-live-tests--updating-mocks)

<!-- mdformat-toc end -->

## Installing dependencies<a name="installing-dependencies"></a>

All the required dependencies can be installed via `pip`, by using the following command:

```shell
pip install pytest pytest-recording
```

Optionally install `pytest-sugar` (prettier output) and `pytest-xdist` (faster test
execution)

```shell
pip install pytest-sugar pytest-xdist
```

## Executing tests<a name="executing-tests"></a>

After installing all the required modules, just call the following command from the root
directory:

```shell
pytest
```

## Running live tests & updating mocks<a name="running-live-tests--updating-mocks"></a>

To speed up the test execution, the network requests are mocked. That means that each HTTP
request does not reach the server, and the response is faked by the
[pytest-recording](https://pypi.org/project/pytest-recording/) module. This greatly
increases the test performance - in my case \<3 seconds vs ~50 seconds, but also may cause
a problem whenever something changes in the real server response. The test-suite on our CI
runs a combination of mocked and live tests.

To run tests with a real network communication use this command:

```shell
pytest --disable-recording
```

Or the faster version (requires `pytest-xdist`)

```shell
pytest -n 4 --disable-recording
```

Whenever the server response will change and affect the tests behavior, the stored
responses can be updated by running

```shell
pytest --record-mode=rewrite
```

Or with `pytest-xdist`

```shell
pytest -n 4 --record-mode=rewrite
```
