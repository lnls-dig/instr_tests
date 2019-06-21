function hplot = tdr_distest_plot(t, data, dly_idx, diel, n, clr)

ref_dly = min(t(dly_idx));
ref_dist = tdr_time2dist(ref_dly, diel);
dist = ((tdr_time2dist(t - ref_dly, diel)))/1e-3;
idx = -ceil(n/3-1):floor(2*n/3);

hplot = zeros(size(data,2), 2);
figure;
for i=1:size(data,2)
    hplot(i,1) = plot(dist(dly_idx(i) + idx), data(dly_idx(i) + idx,i) - data(dly_idx(i),i), 'Color', clr(i,:), 'LineWidth', 2)
    hold all
    hplot(i,2) = plot(dist(dly_idx(i)), 0, 'o', 'Color', clr(i,:), 'LineWidth', 3)
    hold on
end
xlabel(sprintf('Distance relative to %0.3f m [mm]', ref_dist), 'FontSize', 16);
ylabel('Reflection - offset [%]', 'FontSize', 16);
grid on
set(gca, 'FontSize', 16);
set(gca, 'XMinorTick', 'on')
set(gca, 'XMinorGrid', 'on')