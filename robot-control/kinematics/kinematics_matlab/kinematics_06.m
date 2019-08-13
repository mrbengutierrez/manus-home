% The goal of this file is to get the Jacobian matrix

syms l1 l2 l3 l4 d q1 q2


% Define forward kinematics
x_c = l1*cos(q1) - d;
y_c = l1*sin(q1);
x_d = l2*cos(q2) + d;
y_d = l2*sin(q2);

h = sqrt((y_d - y_c)^2 + (x_d - x_c)^2);


delta = acos((l3^2 + h^2 - l4^2) / (2*l3*h));
gamma = atan2( (y_d - y_c) , (x_d - x_c) );

theta_3 = delta + gamma;

% Define the X and Y coordinates of the end-effector as a function of the joint angles (?1?,?3).
XE = x_c + l3*cos(theta_3);
YE = y_c + l3*sin(theta_3);

dXdQ1 = diff(XE,q1)
dXdQ2 = diff(XE,q2)
dYdQ1 = diff(YE,q1)
dYdQ2 = diff(YE,q2)

l1 = 14;
l2 = 14;
l3 = 16;
l4 = 16;
d = 3;
q1 = 3/4*pi;
q2 = pi/4;
dXdQ1 =  - l1*sin(q1) + l3*sin(atan2(l2*sin(q2) - l1*sin(q1), 2*d - l1*cos(q1) + l2*cos(q2)) + acos(((l1*sin(q1) - l2*sin(q2))^2 + (2*d - l1*cos(q1) + l2*cos(q2))^2 + l3^2 - l4^2)/(2*l3*((l1*sin(q1) - l2*sin(q2))^2 + (2*d - l1*cos(q1) + l2*cos(q2))^2)^(1/2))))*(((2*l1*sin(q1)*(2*d - l1*cos(q1) + l2*cos(q2)) + 2*l1*cos(q1)*(l1*sin(q1) - l2*sin(q2)))/(2*l3*((l1*sin(q1) - l2*sin(q2))^2 + (2*d - l1*cos(q1) + l2*cos(q2))^2)^(1/2)) - ((2*l1*sin(q1)*(2*d - l1*cos(q1) + l2*cos(q2)) + 2*l1*cos(q1)*(l1*sin(q1) - l2*sin(q2)))*((l1*sin(q1) - l2*sin(q2))^2 + (2*d - l1*cos(q1) + l2*cos(q2))^2 + l3^2 - l4^2))/(4*l3*((l1*sin(q1) - l2*sin(q2))^2 + (2*d - l1*cos(q1) + l2*cos(q2))^2)^(3/2)))/(1 - ((l1*sin(q1) - l2*sin(q2))^2 + (2*d - l1*cos(q1) + l2*cos(q2))^2 + l3^2 - l4^2)^2/(4*l3^2*((l1*sin(q1) - l2*sin(q2))^2 + (2*d - l1*cos(q1) + l2*cos(q2))^2)))^(1/2) + (((real(l1*cos(q1)) - imag(l1*sin(q1)))/(2*real(d) - real(l1*cos(q1)) + real(l2*cos(q2)) + imag(l1*sin(q1)) - imag(l2*sin(q2))) + ((real(l1*sin(q1)) + imag(l1*cos(q1)))*(real(l2*sin(q2)) - real(l1*sin(q1)) + 2*imag(d) - imag(l1*cos(q1)) + imag(l2*cos(q2))))/(2*real(d) - real(l1*cos(q1)) + real(l2*cos(q2)) + imag(l1*sin(q1)) - imag(l2*sin(q2)))^2)*(2*real(d) - real(l1*cos(q1)) + real(l2*cos(q2)) + imag(l1*sin(q1)) - imag(l2*sin(q2)))^2)/((real(l2*sin(q2)) - real(l1*sin(q1)) + 2*imag(d) - imag(l1*cos(q1)) + imag(l2*cos(q2)))^2 + (2*real(d) - real(l1*cos(q1)) + real(l2*cos(q2)) + imag(l1*sin(q1)) - imag(l2*sin(q2)))^2));
dXdQ1

epsilon = 0.0001;
[b,~] = forwardKinematics(q1+epsilon,q2);
[a,~] = forwardKinematics(q1-epsilon,q2);
dApprox = ( b - a ) / (2*epsilon);
dApprox

%syms x y
%diff(atan2(x,y),x)







% Defines the forward kinematics
function [XE,YE] = forwardKinematics(theta_1,theta_2)
    L_1 = 14;
L_2 = 14;
L_3 = 16;
L_4 = 16;
d = 3;


    % Define forward kinematics
    x_c = L_1*cos(theta_1) - d;
    y_c = L_1*sin(theta_1);
    x_d = L_2*cos(theta_2) + d;
    y_d = L_2*sin(theta_2);

    h = sqrt((y_d - y_c)^2 + (x_d - x_c)^2);
    

    delta = acos((L_3^2 + h^2 - L_4^2) / (2*L_3*h));
    %delta = acos(h/(2*L_3));
    gamma = atan2( (y_d - y_c) , (x_d - x_c) );

    theta_3 = delta + gamma;

    % Define the X and Y coordinates of the end-effector as a function of the joint angles (?1?,?3).
    XE = x_c + L_3*cos(theta_3);
    YE = y_c + L_3*sin(theta_3);
end
