function tdr_settimescale(fid, tdropt, t, scale)

vxi11_write(fid, sprintf(':TIM:POS %g', t));
vxi11_write(fid, sprintf(':TIM:SCAL %g', scale));