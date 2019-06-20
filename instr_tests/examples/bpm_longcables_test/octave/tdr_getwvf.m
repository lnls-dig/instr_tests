function data = tdr_getwvf(fid, tdropt, ch)

data = [];
for i=1:length(ch)
    tic
    % Select trace
    vxi11_write(fid, sprintf(':WAV:SOUR CHAN%d', ch(i)))
    pause(tdropt.sleep_write);
    
    % Ask for trace data
    vxi11_write(fid, ':WAV:DATA?');
    pause(tdropt.sleep_query);
    
    data_temp = textscan(char(vxi11_read(fid, tdropt.nbytes2read)), '%f,');
    data = [data data_temp{1}];        
    toc
end