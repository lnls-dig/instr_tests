function [dly, deriv] = tdr_dlyest(data, arg2)

if isscalar(arg2)
    n = arg2;
    fircoeff = ones(1,n)/n;    
else
    fircoeff = arg2;
    n = (length(fircoeff)+1)/2+1;    
end
 
data_smo = filter(fircoeff, 1, data);
data_smo = data_smo(n:end, :);
[deriv,dly] = max(diff(data_smo));
dly = dly-1;