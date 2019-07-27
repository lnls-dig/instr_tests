function t = tdr_dist2time(dist, diel)

c = 299792458;
propvel = c/sqrt(diel);
t = 2*dist/propvel;