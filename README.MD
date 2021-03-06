## Setup
1. Get python 3.6+
2. virtualenv -p python3.6 env
3. source env/bin/activate
4. clone project
5. cd $PROJECT_ROOT
6. `pip install -r requirements.txt`



## ETH Node mock
ETH Node itself is pretty heavy to setup and launch for development.
So we provide python mocked node to emulate connections and events, required for Node Services.

ETH Node can be launched with `python eth_service_main.py` command

Additional params can be provided, like `python eth_service_main.py --url "0.0.0.0:82" --ws "0.0.0.0:83"`

## Functional tests
Functional tests party covers Multy Back HTTP API.

Requests and responses are validated via [json schemas](https://github.com/Multy-io/multy-back-testing/tree/master/schema/json).
Test cases can be launched with `python func_test_main.py`

By default functional tests are trying to connect to localhost project.
In order to launch tests on another backend instance, `url` parameter can be provided.

`python func_test_main.py --url "http://test.multy.io" --ws "ws://test.multy.io/socket.io/"`

When tests are succeeded, system exit(0) signal will be fired, in other case when tests are failed exit(1) will be triggered

Please, use `func_test_main.py --help` for all available input args list.