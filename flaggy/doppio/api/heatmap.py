import heatmap
from doppio.api.views import show_checkins, parse_checkins

def get_heatmap(u_id):
    c = show_checkins(u_id)
    f = parse_checkins(c)

    hm = heatmap.Heatmap()
    hm.heatmap(f, "%s_heatmap.png" % str(u_id))

    return None