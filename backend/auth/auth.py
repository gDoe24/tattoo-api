import json
from flask import Flask, request, jsonify, _request_ctx_stack, abort
from flask_cors import cross_origin
from functools import wraps
from jose import jwt
from urllib.request import urlopen