function [y, t] = upsample(x, n, nsec, Ts, t0)

if nargin < 4
    Ts = 1;
end

if nargin < 5
    t0 = 0;
end

npts = size(x,1);
ncols = size(x,2);
npts2 = n*npts;

% Fill with zeros in between samples
y = zeros([npts2 ncols]);
y(1:n:end,:) = x;

% Build low pass filter coefficients (CIC)
coeff_1sec = ones(1,n);
coeff = coeff_1sec;
for i=1:nsec-1
     coeff = 1/n*conv(coeff, coeff_1sec);
end

% Filter
y = filter(coeff, 1, y);

% Build time array
dly = (n-1)*(nsec/2)*Ts/n;
t = (0:npts2-1)'*Ts/n + t0 - dly;

% Crop data
ncrop = round((n-1)*nsec);
y = y(ncrop+1:end, :);
t = t(ncrop+1:end);