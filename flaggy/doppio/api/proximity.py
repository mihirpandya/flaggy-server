from math import sqrt, atan, sin, cos, pi

def coord_distance(loc_f, loc_s):

    earth_radius = 6371

    lat_f = loc_f['lat']*2*pi/360
    lat_s = loc_s['lat']*2*pi/360
    lng_f = loc_f['lng']*2*pi/360
    lng_s = loc_s['lng']*2*pi/360

    lng_d = abs(lng_f-lng_s)
    lat_d = abs(lat_f-lat_s)

    num_a = pow(cos(lat_f)*sin(lng_d), 2)
    num_b = pow(cos(lat_s)*sin(lat_f) - sin(lat_s)*cos(lat_f)*cos(lng_d), 2)
    den_a = sin(lat_f)*sin(lat_s)
    den_b = cos(lat_f)*cos(lat_s)*cos(lng_d)


    central_angle_num = sqrt(num_a + num_b)
    central_angle_den = den_a + den_b

    central_angle = atan(central_angle_num/central_angle_den)

    return abs(central_angle*earth_radius)

def comfortable_range(loc_f, loc_s, closest):
    assert(closest < furthest)
    dist = coord_distance(loc_f, loc_s)
    return (closest < dist)