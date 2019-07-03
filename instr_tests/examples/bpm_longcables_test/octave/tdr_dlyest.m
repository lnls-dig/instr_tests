function dly = tdr_dlyest(data, t, method, varargin)

switch method
    case 'fft'
        Fs = 1/(t(2)-t(1));
        if isempty(varargin)
            fc = round(0.01*Fs);
        else
            fc = varargin{1};
        end
        npts = size(data,1)-1; % The data arrays will be shortened by one sample due to diff
        f = (0:npts-1)'/npts*Fs;
        Y = fft(diff(data));
        idx = f <= fc;
        ph = unwrap(angle(Y(idx,:)));
        dly = zeros(size(data,2),1);
        for i=1:size(ph,2)
            dly(i) = -2*pi*f(idx)\ph(:,i);
        end

    case 'deriv'
        if isempty(varargin)
            n = 1;
            nderiv = 1;
        else
            n = varargin{1};
            nderiv = varargin{2};
        end
        fircoeff = ones(1,n)/n;
        data_smo = filter(fircoeff, 1, data);
        data_smo = data_smo(n:end, :);
        if nderiv == 2
            [~,dly_idx] = max(diff(diff(data_smo)));
        else
            [~,dly_idx] = max(diff(data_smo));
            dly_idx = dly_idx-1;
        end
        dly = t(dly_idx);
end