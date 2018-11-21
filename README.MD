## Setup
1. Get python 3.6+
2. clone project
3. cd $PROJECT_ROOT
4. `pip install -r requirements.txt`



## ETH Node mock
ETH Node itself is pretty heavy to setup and launch for development.
So we provide python mocked node to emulate connections and events, required for Node Services.

ETH Node can be launched with `python eth_service_main.py` command

## Functional tests
Functional tests party covers Multy Back HTTP API.

Requests and responses are validated via [json schemas](https://github.com/Multy-io/multy-back-testing/tree/master/schema/json).
Test cases can be launched with `python func_test_main.py`

By default functional tests are trying to connect to localhost project.
In order to launch tests on another backend instans, `url` parameter can be provided.

`python func_test_main.py --url "http://api.multy.io"`