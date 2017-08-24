#!/usr/bin/env python
import redi
import json
print json.dumps(redi.Query(113.3, 23.2))
print json.dumps(redi.QueryVideo(113.3, 23.2))
print json.dumps(redi.Huodong("cbfe4c0e801211e7902500163e082656"))
print json.dumps(redi.Info("cbfe4c0e801211e7902500163e082656"))
