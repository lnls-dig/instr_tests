function dly = tdr_dlyest(data, t, method, varargin)

switch method
    case 'fft'
        Fs = 1/(t(2)-t(1));
        if isempty(varargin)
            fc = round(0.01*Fs);
        else
            fc = varargin{1};
            ndecim = varargin{2};
        end
        [data, t] = downsample(data, ndecim, 2, 1/Fs, t(1));
        Fs = 1/(t(2)-t(1));
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
            ninterp = 1;
        else
            n = varargin{1};
            nderiv = varargin{2};
            ninterp = varargin{3};
        end
        Fs = 1/(t(2)-t(1));
        [data, t] = upsample(data, ninterp, ninterp, 1/Fs, t(1));
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

    case 'edge'
        if isempty(varargin)
            n = 1000;
            ninterp = 1;
            pct =  0.5;
            pct_tol = 0.01;
            nstable = 10;
            dly_guess = zeros(size(data,2), 1);
        else
            n = varargin{1};
            ninterp = varargin{2};
            pct =  varargin{3};
            pct_tol = varargin{4};
            nstable = varargin{5};
            dly_guess = varargin{6};
        end
        Fs = 1/(t(2)-t(1));
        [data, t] = upsample(data, ninterp, ninterp, 1/Fs, t(1));
        Fs = 1/(t(2)-t(1));

        data_roi = zeros(n,size(dly_guess));
        dly = zeros(size(dly_guess));
        for i=1:length(dly)
            aux = find(t <= dly_guess(i));
            dly_idx(i) = aux(end);
            idx = dly_idx(i) - round(n/2) + (-ceil(n/5-1):floor(4*n/5));
            t_roi0 = t(idx(1));
            data_roi(:,i) = data(idx, i);
            data_roi(:,i) = data_roi(:,i) - mean(data_roi(1:nstable,i));
            data_roi(:,i) = data_roi(:,i)./mean(data_roi(end-nstable+1:end,i));
            dly_idx_roi(i) = mean(mean(find(data_roi(:,i) <= pct + pct_tol & data_roi(:,i) >= pct - pct_tol)));
            dly(i) = t_roi0 + (dly_idx_roi(i)'-1)/Fs;
        end
end
