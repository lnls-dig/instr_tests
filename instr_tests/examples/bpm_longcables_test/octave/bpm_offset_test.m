function bpm_offset_test(bpm_name)

path_file = fullfile('~', 'repos_temp', 'instr_tests', 'instr_tests', 'examples', 'bpm_longcables_test', 'octave', 'bpm_offset_data');

clr_direct = [ ...
    0.04 0.58 0.05;
    0.82 0.70 0.10;
    0.04 0.40 0.80;
    0    0    0
    ];

clr_inverted = [ ...
    0.02 0.29 0.02;
    0.41 0.35 0.05;
    0.02 0.20 0.40;
    0.25 0.25 0.25
    ];

    
if nargin < 1
    default_pass = false;
    bpm_name = input('Enter the BPM name and continue [temp]: ','s');
    if isempty(bpm_name)
        bpm_name = 'temp';
    end
else
    default_pass = true;
end

fprintf('Starting test of full RF channel (long cable + RFFE + medium cable + ADC)...\n');

if strcmpi(bpm_name(end-1), '-')
    bpm_name_ = [bpm_name(end-8:end-2) ':DI-BPM'  bpm_name(end-1:end)];
else
    bpm_name_ = [bpm_name(end-6:end) ':DI-BPM'];
    %bpm_name_ = [bpm_name(end-5:end) ':DI-BPM'];
end

pvs_ampl = buildpvnames(bpm_name_, {'AmplA-Mon', 'AmplC-Mon', 'AmplB-Mon', 'AmplD-Mon'});
pvs_rffe_sw = buildpvnames(bpm_name_, 'SwMode-Sel');
pvs_rffe_att = buildpvnames(bpm_name_, 'RFFEAtt-SP');
try
    h = mcaopen(pvs_ampl(1));
catch
    error(sprintf('Could not acquire data from BPM ''%s''. Check the entered BPM name and try again', bpm_name_));
end

data = zeros(40,4);

mcaget(h);
tstamp.init = datestr(mcatime(h), 'yyyy/mm/dd_HH:MM:SS');

tstamp.cable_connect = {};

for i=4:-1:1
    pass = default_pass;
    cond = false(1,6);
    while ~pass
        fprintf('Connect cable  << %d >>  to the RF source...', i);

        for j=1:size(data,1)
            data(j,:) = caget(pvs_ampl);
            pause(0.1);
        end
        
        a1 = mean(data(1:5,:));
        a2 = mean(data(end-4:end,:));
        g = a2./a1;
        [~,max_i] = max(abs(g));
        
        cond(1) = mean(data(1:5,i)) < 1e4;
        cond(2) = any(diff(data(2:end,i)) > 1e3);
        cond(3) = g(i) > 5;
        cond(4) = i == max_i;
        %aux = a2(i) > a1(i+1:end);
        %cond(5) = all(aux) || isempty(aux);    % FIXME: check if isempty is needed
        cond(5) = all(a2(i)./a1(1:i-1) > 5);
        cond(6) = all(a1(i)./a2(i+1:end) < 5);
        
        if all(cond)
            mcaget(h);
            tstamp.cable_connect{i} = datestr(mcatime(h), 'yyyy/mm/dd_HH:MM:SS');
            pass = true;
            fprintf(' CONNECTED!\n');            
        else
            fprintf('\n');
        end
    end
end

if nargin < 1
    input('Press <Enter> to start offset test: ','s');
end

rffeatt_origstate = caget(pvs_rffe_att);
rffesw_origstate = caget(pvs_rffe_sw);

rffe_att = [0:5:30];
for i=1:length(rffe_att)
    caput(pvs_rffe_att, rffe_att(i));
    caput(pvs_rffe_sw, 1);
    pause(0.3);
    mcaget(h);
    tstamp.sw_direct{i} = datestr(mcatime(h), 'yyyy/mm/dd_HH:MM:SS');
    pause(5);
    caput(pvs_rffe_sw, 2);
    pause(0.3);
    mcaget(h);
    tstamp.sw_inverted{i} = datestr(mcatime(h), 'yyyy/mm/dd_HH:MM:SS');
    pause(5);
end
mcaget(h);
tstamp.end = datestr(mcatime(h), 'yyyy/mm/dd_HH:MM:SS');
caput(pvs_rffe_att, rffeatt_origstate);
caput(pvs_rffe_sw, rffesw_origstate);

mcaclose(h);

% Save results to JSON file
date_time = now;
date_time_filename = datestr(date_time, 'yyyy-mm-dd_HH-MM-SS');
filename = sprintf('bpm_offset_%s_%s.json', bpm_name, date_time_filename);

fprintf('Saving results to file ''%s''...\n\n', filename);

result.bpm_name = bpm_name;
result.tstamp = tstamp;
result.rffe_att = rffe_att;

opt.FileName = fullfile(path_file, filename);
savejson('', result, opt);
