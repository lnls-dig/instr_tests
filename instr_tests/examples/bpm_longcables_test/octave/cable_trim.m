tdr_ip = '10.15.0.164';
swbox_ip = '10.15.0.103';

cable_diel = 1.56;
tdr_source = 'RESP3';
npts_plot = 1000;
upsample_factor = 10;
%dlyest_method =  'deriv'; dlyest_args = {20,1};
dlyest_method =  'fft'; dlyest_args = {75e6, 2};
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

% Pre-allocate data array
data = zeros(length(t), 4);

% Update each length measurement at user's request
r = 'a';
while true
    switch r
        case 'q'
            break
        case 'a'
            ch = 1:4;
        otherwise
            if isempty(r)
                ch = last_ch;
            else
                rnum = str2double(r);
                if rnum >= 1 && rnum <= 4 && mod(rnum,1) == 0
                    ch = rnum;
                else
                    fprintf('Wrong option. Choose among 1/2/3/4/a/q.\n');
                    continue
                end
            end
    end
    
    for i=ch
        fprintf('Measuring cable %d... ', i);
        swbox_setsw(swbox_ip, 'A', i);
        pause(2);
        data(:,i) = tdr_getdata(fid, tdropt, tdr_source);
        fprintf('done.\n');
    end
    
    dly = tdr_dlyest(data, t, dlyest_method, dlyest_args{:});
    if exist('hplot', 'var')
        try
            for i=1:length(hplot)
                get(hplot(i), 'Children');
            end
            valid_hplot = 1;
        catch
            valid_hplot = 0;
        end
    else
        valid_hplot = 0;
    end
    if valid_hplot
        tdr_distest_plot(t, data, dly, cable_diel, npts_plot, [], 'update', hplot);
    else
        hplot = tdr_distest_plot(t, data, dly, cable_diel, npts_plot, clr);
    end
    title(cable_name);
    tdr_distest_print(dly, cable_diel);
    last_ch = ch(end);
    r = input(sprintf('Choose cable measurement to be updated (1/2/3/4) or ''a'' to update all or ''q'' to quit and save results [%d]: ', last_ch),'s');
end

vxi11_close(fid);

cable_length = tdr_time2dist(dly, cable_diel);

% Save results to JSON file
filename = sprintf('cable_trim_%s_%s.json', cable_name, datestr(now, 'yyyy-mm-dd_HH-MM-SS'));

fprintf('Saving results to file ''%s''...\n\n', filename);

result.cable_name = cable_name;
result.cable_length = cable_length';
result.refplane = refplane;
result.t = t';
result.data = data';
result.cable_dielectric = cable_diel;

opt.FileName = filename;
savejson('', result, opt);
