#!/bin/bash

pg_dump \
  --clean \
  --blobs \
  --dbname=locations \
  --encoding=utf-8 \
  --if-exists \
  --no-owner \
  --quote-all-identifiers \
  --password \
  --username=benji

