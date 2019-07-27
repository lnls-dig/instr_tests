function [y, t] = downsample(x, n, nsec, Ts, t0)

if nargin < 4
    Ts = 1;
end

if nargin < 5
    t0 = 0;
end

npts = floor(size(x,1)/n)*n;
x = x(1:npts,:);

% Build low pass filter coefficients (CIC)
coeff_1sec = ones(1,n)/n;
coeff = coeff_1sec;
for i=1:nsec-1
     coeff = conv(coeff, coeff_1sec);
end

% Filter
y = filter(coeff, 1, x);

% Build time array
dly = n*(nsec/2)*Ts;
t = (0:npts-1)'*Ts + t0 - dly;

% Crop data
ncrop = round(n*nsec);
y = y(ncrop+1:end, :);
t = t(ncrop+1:end);

% Decimate
y = y(1:n:end,:);
t = t(1:n:end,:);