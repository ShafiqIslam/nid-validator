from app.common.helpers import log


def hasMatch(match):
    if match:
        groups = match.groups()
        log(groups)
        index = 0
        for i in groups:
            if i is not None:
                return index, i.strip()
            index += 1
    return None


def getEmptyOutput(indexes):
    output = {}
    for item in indexes:
        output[item] = None
    return output
