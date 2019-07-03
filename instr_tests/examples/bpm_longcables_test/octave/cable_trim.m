tdr_ip = '10.15.0.164';
swbox_ip = '10.15.0.103';

cable_diel = 1.56;
tdr_source = 'RESP3';
dlyest_fc = 75e6;
npts_plot = 1000;
upsample_factor = 10;
clr = [ ...
    0.04 0.58 0.05;
    0.82 0.70 0.10;
    0.04 0.40 0.80;
    0    0    0
    ];

cable_name = input('Enter the cable name and continue [temp]: ','s');
if isempty(cable_name)
    cable_name = 'temp';
end

fprintf('Starting cable trimming procedure...\n');

try
    fid = vxi11(tdr_ip);
catch err
    error('Could not connect to TDR device at IP address ''%s''', tdr_ip);
end

tdropt = tdr_options;

% Retrieve TDR reference plane in seconds
refplane = tdr_getrefplane(fid, tdropt, tdr_source);

% Retrive time array
t_orig = tdr_gettime(fid, tdropt);
t = t_orig-refplane;
dt = t(2)-t(1);

% First length measurement for all cables
data = [];
for i=1:4
    fprintf('Measuring cable %d...', i);
    swbox_setsw(swbox_ip, 'A', i);
    pause(2);
    data = [data tdr_getdata(fid, tdropt, tdr_source)];
    fprintf('done.\n');
end
dly = tdr_dlyest(data, t, dlyest_fc);
hplot = tdr_distest_plot(t, data, dly, cable_diel, npts_plot, clr);
tdr_distest_print(dly, cable_diel);

% Update each length measurement at user's request
last_ch = i;
while true
    r = input(sprintf('Choose cable measurement to be updated (1/2/3/4) or ''q'' to quit [%d]: ', last_ch),'s');
    switch r
        case 'q'
            break
        otherwise
            if isempty(r)
                i = last_ch;
            else
                rnum = str2double(r);
                if rnum >= 1 && rnum <= 4 && mod(rnum,1) == 0
                    i = rnum;
                else
                    fprintf('Wrong option. Choose among 1/2/3/4/q.\n');
                    continue
                end
            end
    end
    
    fprintf('Measuring cable %d... ', i);
    swbox_setsw(swbox_ip, 'A', i);
    pause(2);
    data(:,i) = tdr_getdata(fid, tdropt, tdr_source);
    fprintf('done.\n');
    
    dly = tdr_dlyest(data, t, dlyest_fc);
    tdr_distest_plot(t, data, dly, cable_diel, npts_plot, [], 'update', hplot);
    tdr_distest_print(dly, cable_diel);
    last_ch = i;
end

vxi11_close(fid);

% Save results to JSON file
filename = sprintf('cable_trim_%s_%s.json', cable_name, datestr(now, 'yyyy-mm-dd_HH-MM-SS'));

fprintf('Saving results to file ''%s''...\n\n', filename);

result.refplane = refplane;
result.t = t';
result.data = data';
result.cable_dielectric = cable_diel;

opt.FileName = filename;
savejson('', result, opt);
