
% Failed to solve forward kinematics

syms L_1 L_2 L_3 L_4 theta_1 theta_3 XE YE d

% % Define joint angle lengths
% L_1 = 14;
% L_2 = 16;
% L_3 = 14;
% L_4 = 16;
% d = 3;

% Define forward kinematics
x_b = L_1*cos(theta_1) - d;
y_b = L_1*sin(theta_1);
x_d = L_3*cos(theta_3) + d;
y_d = L_3*sin(theta_3);

h = sqrt((y_d - y_b)^2 + (x_d - x_b)^2);

delta = acos((L_2^2 + h^2 - L_4^2) / (2*L_2*h));
gamma = atan2( (y_d - y_b) , (x_d - x_b) );

theta_2 = delta + gamma;

% Define the X and Y coordinates of the end-effector as a function of the joint angles (?1?,?3).
XE_RHS = x_b + L_2*cos(theta_2);
YE_RHS = y_b + L_2*sin(theta_2);

% Convert the symbolic expressions into MATLAB functions.
variables = [L_1, L_2, L_3, L_4, d, theta_1, theta_3];
XE_MLF = matlabFunction(XE_RHS,'Vars',variables);
YE_MLF = matlabFunction(YE_RHS,'Vars',variables);

% Define forward kinematic equations
XE_EQ = XE == XE_RHS;
YE_EQ = YE == YE_RHS;

% Solve for ?1 and ?3 .
S = solve([XE_EQ, YE_EQ], [theta_1, theta_3]);


