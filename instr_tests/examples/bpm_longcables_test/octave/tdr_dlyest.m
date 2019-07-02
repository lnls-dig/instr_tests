function [dly, deriv] = tdr_dlyest(data, arg2, nderiv)

if isscalar(arg2)
    n = arg2;
    fircoeff = ones(1,n)/n;
else
    fircoeff = arg2;
    n = (length(fircoeff)+1)/2+1;
end

if nargin < 3 || isempty(nderiv)
    nderiv = 1;
end

data_smo = filter(fircoeff, 1, data);
data_smo = data_smo(n:end, :);

if nderiv == 2
    [deriv,dly] = max(diff(diff(data_smo)));
else
    [deriv,dly] = max(diff(data_smo));
    dly = dly-1;
end
