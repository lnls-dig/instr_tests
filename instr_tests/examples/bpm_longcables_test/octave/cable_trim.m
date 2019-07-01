tdr_ip = '10.15.0.164';
swbox_ip = '10.15.0.103';

cable_diel = 1.56;
tdr_source = 'RESP3';
dlyest_navg = 20;
npts_plot = 20;
clr = [ ...
    0.04 0.58 0.05;
    0.82 0.70 0.10;
    0.04 0.40 0.80;
    0    0    0
    ];

fid = vxi11(tdr_ip);
tdropt = tdr_options;

% Retrieve TDR reference plane in seconds
refplane = tdr_getrefplane(fid, tdropt, tdr_source);

% Retrive time array
t = tdr_gettime(fid, tdropt);

% First length measurement for all cables
dly_idx = zeros(4,1);
deriv = zeros(4,1);
cable_dly = zeros(4,1);
data = [];
for i=1:4
    swbox_setsw(swbox_ip, 'A', i);
    pause(2);
    data = [data tdr_getdata(fid, tdropt, tdr_source)];
end
[dly_idx, deriv] = tdr_dlyest(data, dlyest_navg);
[hplot, ref_dly] = tdr_distest_plot(t-refplane, data, dly_idx, cable_diel, npts_plot, clr);

% Update each length measurement at user's request
last_ch = i;
while true
    r = input(sprintf('Choose cable measurement to be updated (1/2/3/4) [default = %d (last value)] and press <Enter>. Press ''q'' + <Enter> to quit): \n', last_ch),'s');
    switch r
        case 'q'
            break
        otherwise
            if isempty(r)
                i = last_ch;
                fprintf('Selecting default (cable #%d)...\n',i);
            else
                rnum = str2double(r);
                if rnum >= 1 && rnum <= 4 && mod(rnum,1) == 0
                    i = rnum;
                    fprintf('Selected cable #%d.\n',i);
                else
                    fprintf('Wrong option. Choose among 1/2/3/4.\n');
                    continue
                end
            end
    end
    
    swbox_setsw(swbox_ip, 'A', i);
    pause(2);
    data(:,i) = tdr_getdata(fid, tdropt, tdr_source);
    [dly_idx, deriv] = tdr_dlyest(data, dlyest_navg);
    tdr_distest_plot(t-refplane, data, dly_idx, cable_diel, npts_plot, [], 'update', hplot);
    last_ch = i;
end

vxi11_close(fid);
