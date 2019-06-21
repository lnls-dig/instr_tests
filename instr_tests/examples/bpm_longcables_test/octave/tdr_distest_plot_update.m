function tdr_distest_plot_update(hplot, t, data, dly_idx, diel, n)

[ref_dly, ref_i] = min(t(dly_idx));
ref_dist = tdr_time2dist(ref_dly, diel);
dist = ((tdr_time2dist(t - ref_dly, diel)))/1e-3;
idx = -ceil(n/3-1):floor(2*n/3);

for i=1:size(data,2)
    set(hplot(i,1), 'XData', dist(dly_idx(i) + idx));
    set(hplot(i,1), 'YData', data(dly_idx(i) + idx, i) - data(dly_idx(i), i));
    set(hplot(i,2), 'XData', dist(dly_idx(i)));
end

for i=1:size(data,2)
    leg{i} = sprintf('\\Deltat_{%d\\rightarrow%d}: %0.0f mm\n', ref_i, i, dist(dly_idx(i)));
end
legend(leg, 'Location', 'NorthWest')