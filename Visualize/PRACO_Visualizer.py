import numpy as np, pandas as pd




# Script for reading PRACO encoder encoderData
clear()
clc()
# encoderData = dlmread(mstring('Encoder_data2.txt'), mstring(','), 1, 0)
encoderData = np.genfromtxt("Encoder_data2.txt", delimiter=",")

n = 7
# angle = encoderData(1:n-1,n+1:end,53);
angle = encoderData(mslice[:], 53)
angle(angle == 0).lvalue = mcat([])

index = (mslice[1:size(angle, 1)]).cT
count = interp1(index(mslice[6:6:end]), encoderData(mslice[7:7:end], 58), index, mstring('spline'))

quadBL = encoderData(mslice[:], 54)
quadBH = encoderData(mslice[:], 55)
removalList = mslice[n:n:size(encoderData, 1)]
quadBL(removalList).lvalue = mcat([])
quadBH(removalList).lvalue = mcat([])
quadBL(quadBL > 0).lvalue = 1
quadBH(quadBH > 0).lvalue = 1
quadD = quadBL + 2 * quadBH + 1

figure()
[haxes, hline1, hline2] = plotyy(count, angle, count, quadD)
ylabel(haxes(1), mstring('Angle (\\circ)'))# label left y-axis
ylabel(haxes(2), mstring('Quadrant'))# label right y-axis
xlabel(haxes(2), mstring('Raw Counts'))# label x-axis
axis(haxes(1), mcat([count(1), count(end) - 0.5 * 120, 360 + 0.5 * 120]))
axis(haxes(2), mcat([count(1), count(end), 0.5, 4.5]))
set(hline1, mstring('LineWidth'), 2)
set(hline2, mstring('LineStyle'), mstring('--'), mstring('LineWidth'), 2)
set(haxes(1), mstring('YTick'), mcat([0, 90, 180, 270]))
set(haxes(2), mstring('YTick'), mcat([1, 2, 3, 4]))



# radData = dlmread(mstring('Radiometer_Data_cable1_2.txt'), mstring(','), 1, 0)
radData = np.genfromtxt("Radiometer_Data_cable1_2.txt", delimiter=",")

radCount = radData(mslice[:], 27)
sample1 = radData(mslice[:], mslice[1:12])
sample2 = radData(mslice[:], mslice[14:25])

radAve = (sample1 + sample2) / 2

figure()
plot(radAve