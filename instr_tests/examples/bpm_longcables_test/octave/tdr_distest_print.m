function [rel_dist, ref_dist] = tdr_distest_print(cable_dly, diel)
  
cable_dist = tdr_time2dist(cable_dly, diel)/1e-3;
[ref_cable_dist, ref_i] = min(cable_dist);
cable_dist_rel_mm = (cable_dist - ref_cable_dist);

fprintf('Estimated cable lengths (relative):\n');
for i=1:length(cable_dist_rel_mm)
	fprintf('Cable #%d: %0.2f mm\n', i, cable_dist_rel_mm(i));
end
fprintf('Reference distance (cable #%d): %0.2f mm\n\n',ref_i, ref_cable_dist);