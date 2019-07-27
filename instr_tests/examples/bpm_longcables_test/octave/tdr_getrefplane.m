function refplane = tdr_getrefplane(fid, tdropt, source)
  
vxi11_write(fid, sprintf(':TDR:%s:RPL?', source));
refplane = str2double(char(vxi11_read(fid, tdropt.nbytes2read)));