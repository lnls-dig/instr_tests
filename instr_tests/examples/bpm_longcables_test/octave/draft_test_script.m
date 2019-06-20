min_cable_length = 10;
max_cable_length = 70;
diel = 1.56;

trig_dly = tdr_dist2time(min_cable_length, diel) - 1e-9;
ch = 3;
navg = 40;

fid = vxi11('10.15.0.164');
tdropt = tdr_options;

refplane =  tdr_getrefplane(fid, tdropt, ch);

tdr_settimescale(fid, tdropt, trig_dly, 200e-9)
pause(1)

for i=1
    swbox_setsw('10.15.0.135', 'A', i);
    pause(2);
    data = tdr_getwvf(fid, tdropt, ch);
    t = tdr_gettime(fid, tdropt, ch);
    cable_dly(i) = t(round(tdr_dlyest(data, navg)));
end
cable_dly_refplane = (cable_dly-refplane)/1e-9

tdr_settimescale(fid, tdropt, min(cable_dly) -1e-9, 1e-9);
pause(1)
for i=1
    swbox_setsw('10.15.0.135', 'A', i);
    pause(2);
    data = tdr_getwvf(fid, tdropt, ch);
    t = tdr_gettime(fid, tdropt);
    cable_dly2(i) = t(round(tdr_dlyest(data, navg)));
end
cable_dly_refplane2 = (cable_dly2-refplane)/1e-9

vxi11_close(fid);
