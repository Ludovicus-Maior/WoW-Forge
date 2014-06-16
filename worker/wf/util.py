#!/usr/bin/env python





def IsLimitExceeded(data):
    if 'status' in data and data['status'] == "nok":
        if 'reason' in data and data['reason'] == "Daily limit exceeded":
            return True




