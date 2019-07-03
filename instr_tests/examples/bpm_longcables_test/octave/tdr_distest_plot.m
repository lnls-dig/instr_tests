function hplot = tdr_distest_plot(t, data, dly, diel, n, clr, call_type, hplot)

if nargin < 7 || isempty(call_type)
    call_type = 'first';
end

[ref_dly, ref_i] = min(dly);
ref_dist = tdr_time2dist(ref_dly, diel);
dist = ((tdr_time2dist(t - ref_dly, diel)))/1e-3;
idx = -ceil(n/3-1):floor(2*n/3);
dist_cable = tdr_time2dist(dly - ref_dly, diel)/1e-3;

dly_idx = zeros(size(dly));
ampl_dist_cable = zeros(size(dly));
for i=1:length(dly)
    aux = find(t <= dly(i));
    dly_idx(i) = aux(end);
    ampl_dist_cable(i) = interp1(dist, data(:,i), dist_cable(i));
end

if strcmp(call_type, 'first')
    hplot = zeros(size(data,2), 3);
    figure;
    for i=1:size(data,2)
        hplot(i,1) = plot(dist(dly_idx(i) + idx), data(dly_idx(i) + idx,i), 'Color', clr(mod(i-1, size(clr,1))+1,:), 'LineWidth', 2);
        hold all
    end
    for i=1:size(data,2)
        hplot(i,2) = plot(dist_cable(i), ampl_dist_cable(i), 'o', 'Color', clr(mod(i-1, size(clr,1))+1,:), 'LineWidth', 3);
    end
    ylabel('Reflection [%]', 'FontSize', 16);
    grid on
    set(gca, 'FontSize', 16);
    set(gca, 'XMinorTick', 'on')
    set(gca, 'XMinorGrid', 'on')
    
elseif strcmp(call_type, 'update')
    for i=1:size(data,2)
        set(hplot(i,1), 'XData', dist(dly_idx(i) + idx));
        set(hplot(i,1), 'YData', data(dly_idx(i) + idx, i));
        set(hplot(i,2), 'XData', dist_cable);
        set(hplot(i,2), 'YData', ampl_dist_cable);
    end
end

xlabel(sprintf('Distance relative to %0.3f m [mm]', ref_dist), 'FontSize', 16);
for i=1:size(data,2)
    leg{i} = sprintf('Cable #%d, \\Deltat_{%d\\rightarrow%d}: %0.0f mm\n', i, ref_i, i, dist_cable(i));
end
legend(leg, 'Location', 'NorthWest')
