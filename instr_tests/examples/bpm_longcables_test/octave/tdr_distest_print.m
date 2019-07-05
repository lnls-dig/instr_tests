function [rel_dist, ref_dist] = tdr_distest_print(cable_dly, diel)
  
cable_dist = tdr_time2dist(cable_dly, diel)/1e-3;
[ref_cable_dist, ref_i] = min(cable_dist);
cable_dist_rel_mm = (cable_dist - ref_cable_dist);
fprintf('Estimated distances (relative to reference distance):\n    Cable #1: %0.2f mm\n    Cable #2: %0.2f mm\n    Cable #3: %0.2f mm\n    Cable #4: %0.2f mm\n\nReference distance (cable #%d): %0.2f mm\n\n', cable_dist_rel_mm(1), cable_dist_rel_mm(2), cable_dist_rel_mm(3), cable_dist_rel_mm(4), ref_i, ref_cable_dist);