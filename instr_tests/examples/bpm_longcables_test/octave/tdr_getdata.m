function data = tdr_getdata(fid, tdropt, source)

% Select trace
vxi11_write(fid, sprintf(':WAV:SOUR %s', source));
pause(tdropt.sleep_write);

% Ask for trace data
vxi11_write(fid, ':WAV:DATA?');
pause(tdropt.sleep_query);

data = textscan(char(vxi11_read(fid, tdropt.nbytes2read)), '%f,');
data = data{1};