tdr_ip = '10.15.0.164';
swbox_ip = '10.15.0.103';

cable_diel = 1.56;
tdr_source = 'RESP3';
npts_plot = 1000;
upsample_factor = 10;
dlyest_args_deriv = {50, 1, 15};
dlyest_args_edge = {30000, 15, 0.5, 0.01, 500, [0; 0; 0; 0]};
clr = [ ...
    0.04 0.58 0.05;
    0.82 0.70 0.10;
    0.04 0.40 0.80;
    0    0    0
    ];
nmeas = 5;
tdr_meas = false;

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
refplane = tdr_get(fid, tdropt, sprintf(':TDR:%s:RPL', tdr_source), 'double');

% Retrive time array
t_orig = tdr_gettime(fid, tdropt);
t = t_orig-refplane;
dt = t(2)-t(1);

if tdr_meas
    % Set default scale (full view)
    tdr_set(fid, tdropt, ':TIM:RANG', t_orig(end)-t_orig(1));
    tdr_set(fid, tdropt, ':TIM:POS', t_orig(1));
    
    % Pre-allocate arrays
    dly2 = zeros(4,1);
    dly2_std = zeros(4,1);
end

% Pre-allocate data array
data = zeros(length(t), 4);

% Update each length measurement at user's request
r = 'a';
while true
    valid_option = true;
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
                    valid_option = false;
                end
            end
    end
    
    if valid_option
        for i=ch
            fprintf('Measuring cable %d... ', i);
            swbox_setsw(swbox_ip, 'A', i);
            pause(2);
            data(:,i) = tdr_getdata(fid, tdropt, tdr_source);
            fprintf('done.\n');

            if tdr_meas
                tdr_set(fid, tdropt, ':TIM:RANG', t_orig(end)-t_orig(1));
                tdr_set(fid, tdropt, ':TIM:POS', t_orig(1));
                pause(0.5);
                tedge(i) = tdr_get(fid, tdropt, sprintf(':MEASURE:TEDGE? LOW,+1,%s', tdr_source), 'double');
                tdr_set(fid, tdropt, ':TIM:RANG', 50e-9);
                tdr_set(fid, tdropt, ':TIM:POS', tedge(i) - 5e-9 + refplane);
                pause(0.5);
                
                aux = zeros(nmeas,1);
                for j=1:nmeas
                    aux(j) = tdr_get(fid, tdropt, sprintf(':MEASURE:TEDGE? MIDD,+1,%s', tdr_source), 'double');
                    pause(1);
                end
                dly2(i) = mean(aux);
                dly2_std(i) = std(aux);
            end
        end

        if tdr_meas
            tdr_set(fid, tdropt, ':TIM:RANG', t_orig(end)-t_orig(1));
            tdr_set(fid, tdropt, ':TIM:POS', t_orig(1));
        end
        
        dly_guess = tdr_dlyest(data, t, 'deriv', dlyest_args_deriv{:});
        dlyest_args_edge{6} = dly_guess;
        dly = tdr_dlyest(data, t, 'edge', dlyest_args_edge{:});
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
    end
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
