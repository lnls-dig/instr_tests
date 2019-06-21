function refplane = tdr_getrefplane(fid, tdropt, ch)
  
vxi11_write(fid, sprintf(':TDR:RESPonse%d:RPL?',ch));
refplane = str2double(char(vxi11_read(fid, tdropt.nbytes2read)));