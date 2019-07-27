function swbox_setsw(ip, swname, swvalue, verbose)

if nargin < 4
    verbose = 0;
end

if ischar(swname)
    swname = {swname};
end

fid = tcp(ip,23);
tcp_read(fid, 100, 1);
for i=1:length(swname)
    msg = sprintf('SP4T%s:STATE:%d\n', swname{i}, swvalue(i));
    tcp_write(fid, msg);
    pause(1);
    r = tcp_read(fid, 100, 1);
    if verbose
        fprintf('Reply for message ''%s'': %s', msg, r);
    end
end
fclose(fid);
