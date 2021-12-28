#!/bin/bash

pytest --cov-report=term-missing --cov=api/ --disable-network -x --cov-fail-under=80 || exit 1