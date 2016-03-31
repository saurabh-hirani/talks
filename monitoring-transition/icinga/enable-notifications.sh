#!/bin/bash
curl -X POST  -H "Content-type: application/json;" -d '{"host": "app-1", "services_too": true}' http://localhost:6315/enable_notifications/
