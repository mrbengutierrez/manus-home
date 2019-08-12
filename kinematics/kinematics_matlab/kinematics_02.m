
% Failed to turn inverse kinematics into forward kinematics
syms L_1 L_2 L_3 L_4 d theta_1 theta_2 XE YE

theta_1_RHS = pi - atan2(YE,XE+d) + acos((L_2^2 - L_1^2 - (XE+d)^2 - YE) / (2*L_1*sqrt((XE+d)^2 + YE^2)) );
theta_3_RHS = atan2(YE,XE-d) - acos(((XE-d)^2 + YE^2 + L_3^2 - L_4^2) / (2*L_3*sqrt((XE - d)^2 + YE^2)));

theta_1_eq = theta_1 == theta_1_RHS;
theta_3_eq = theta_3 == theta_3_RHS;

S = solve([theta_1_eq, theta_3_eq], [XE, YE]);