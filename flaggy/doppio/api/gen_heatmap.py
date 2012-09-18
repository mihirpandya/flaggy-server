from heatmap import Heatmap
from doppio.api.controllers import __show_checkins, success, error

def parse_checkins(checkins_obj):
    result = [ ]
    checkins = checkins_obj['checkins']

    i = 0

    while (i < len(checkins)):
        item = checkins[i]
        lat = item['lat']
        lng = item['lng']

        coord = (lat, lng)
        result.append(coord)
        i+=1

    return result

def get_heatmap(u_id):
    c = __show_checkins(u_id)
    f = parse_checkins(c)

    hm = Heatmap()
    hm.heatmap(f, "%s_heatmap.png" % str(u_id))

    return success("Generated heatmap.")