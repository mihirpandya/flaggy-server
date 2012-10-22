## SUCCESS/ERROR RESPONSES ##

def success(msg):
    return {'status': 'success', 'msg': msg}

def error(msg):
    return {'status': 'error', 'msg': msg}

def is_Success(obj):
    return (obj['status'] == "success")

def is_Error(obj):
    return (obj['status'] == "error")

def get_Msg(obj):
	return obj['msg']
