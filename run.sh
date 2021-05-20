#!/bin/sh
gunicorn -w 4 `
`--bind 0.0.0.0:10001 `
`netpalm-admin:app --log-level debug
