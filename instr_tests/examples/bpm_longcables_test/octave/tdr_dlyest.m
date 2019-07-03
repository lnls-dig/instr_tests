function dly = tdr_dlyest(data, t, fc)

npts = size(data,1);
Ts = t(2)-t(1);
Y = fft(diff(data));
f = (0:npts-1)'/npts/Ts;
idx = f <= fc;
ph = unwrap(angle(Y(idx,:)));
dly = zeros(1, size(data,2));
for i=1:size(ph,2)
    dly(i) = -2*pi*f(idx)\ph(:,i);
end