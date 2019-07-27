function dist = tdr_time2dist(t, diel)

c = 299792458;
propvel = c/sqrt(diel);
dist = t*propvel/2;