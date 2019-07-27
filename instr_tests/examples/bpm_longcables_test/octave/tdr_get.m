function val = tdr_get(fid, tdropt, cmd, type)

if nargin < 4
    type = 'char';
end

if isempty(strfind(cmd, '?'))
    cmd = [cmd '?'];
end

vxi11_write(fid, cmd);
val_txt = char(vxi11_read(fid, tdropt.nbytes2read));

switch type
    case 'double'
        val = str2double(val_txt);
    otherwise
        val = val_txt;
end