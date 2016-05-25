# RESTful API with Python and Flask

In recent years REST (REpresentational State Transfer) has emerged as the standard architectural design for web services and web APIs.

This is a simple RESTful web service using Python and the Flask microframework for retreiving Queues stats from DPDK app.

## Installation
### 1.  Clone the repos
```
git clone https://github.com/6WIND/fp_RESTful.git
```
### 2. Install Flask in a virtual environment
-  If you don't have `virtualenv` installed in your system, you can do it with:
```
pip install virtualenv
```
- or download and install for [source](https://pypi.python.org/pypi/virtualenv).

Install dependencies:
```
cd fp_restful
virtualenv flask
flask/bin/pip install flask flask_restful
```

## Usage
### 1. Run the APP
To run this application we have to execute `fp-restful.py`:
```
./fp-restful.py
```
- If you don't have a **_Data file_**, you can generate a random one using `fp-cli`, on your browser go to:
```
<server_ip>:<port>/fp-cli/gen
```
Then you have a new random Data file in you repo every time you refresh the link.

### 2. Dump data struc in JSON
```
<server_ip>:<port>/qstats
```

