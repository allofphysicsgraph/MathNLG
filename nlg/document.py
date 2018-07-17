# accepts knowledge source ks
# returns document plan dp
def documentPlanner(ks) :
    # validate input
    if ks.tag != 'source' :
        raise ValueError('Document planner expects root of knowledge source')
    # document plan
    dp = {}
    dp['definition'] = []
    for child in ks :
        dp[child.tag].append(child)
    return dp
