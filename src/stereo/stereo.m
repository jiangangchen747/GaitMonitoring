clear; clc; close all;

xyposition = readtable('1 marker position in image.csv');
numOfRow= size(xyposition, 1);

% Camera parameters
load('matlab.mat')

results = [];
for i = 1:numOfRow
    xyPair = xyposition(i,:);
    object1 = [xyPair(1, "Var1"), xyPair(1, "Var2")];
    object2 = [xyPair(1, "Var3"), xyPair(1, "Var4")];
    object1 = object1{:,:};
    object2 = object2{:,:};

    position3d = triangulate(object1, object2, stereoParams);
    positioninMeter = position3d/10; % /10:cm; /1000:m;
    totalDis = sqrt(positioninMeter(2)^2 + positioninMeter(3)^2);

    position = horzcat(positioninMeter, totalDis);
    results = vertcat(results, position)
end

csvwrite('2 stereo distance.csv', results)