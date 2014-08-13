#!/bin/sh
# run the flake8 tool, but ignore "line too long" errors
flake8 --ignore=E501 TextImager.py
