function tdr_set(fid, tdropt, cmd, val)

if isnumeric(val)
    val_txt = sprintf(' %g', val);
elseif ischar(val)
    val_txt = [' ' val];
else
    error('Invalid data type');
end

vxi11_write(fid, [cmd val_txt]);