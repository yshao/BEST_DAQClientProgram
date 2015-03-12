% Script for reading PRACO encoder encoderData
clear
clc
encoderData = dlmread('Encoder_data2.txt',',',1,0);

n = 7;
% angle = encoderData(1:n-1,n+1:end,53);
angle = encoderData(:,53);
angle(angle==0) = [];

index = (1:size(angle,1))';
count = interp1(index(6:6:end),encoderData(7:7:end,58),index,'spline');

quadBL = encoderData(:,54);
quadBH = encoderData(:,55);
removalList = n:n:size(encoderData,1);
quadBL(removalList) = [];
quadBH(removalList) = [];
quadBL(quadBL>0) = 1;
quadBH(quadBH>0) = 1;
quadD = quadBL + 2*quadBH + 1;

figure
[haxes,hline1,hline2] = plotyy(count,angle,count,quadD);
ylabel(haxes(1),'Angle (\circ)') % label left y-axis
ylabel(haxes(2),'Quadrant') % label right y-axis
xlabel(haxes(2),'Raw Counts') % label x-axis
axis(haxes(1),[count(1) count(end) -0.5*120 360+0.5*120])
axis(haxes(2),[count(1) count(end) 0.5 4.5])
set(hline1,'LineWidth',2);
set(hline2,'LineStyle','--','LineWidth',2);
set(haxes(1),'YTick',[0 90 180 270])
set(haxes(2),'YTick',[1 2 3 4])



radData = dlmread('Radiometer_Data_cable1_2.txt',',',1,0);

radCount = radData(:,27);
sample1 = radData(:,1:12);
sample2 = radData(:,14:25);

radAve = (sample1+sample2)/2;

figure
plot(radAve)