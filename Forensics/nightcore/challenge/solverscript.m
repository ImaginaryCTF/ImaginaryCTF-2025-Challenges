%% create the challenge
clc;clear
%% open the original file
[y,Fs] = audioread('nightcore.mp3');
%sound(y,Fs)
T = 1/Fs;             % Sampling period       
L = length(y);        % Length of signal
%t = (0:L-1)*T;        % Time vector
Y = fft(y);
P2 = abs(Y/L);
P1 = P2(1:L/2+1);
P1(2:end-1) = 2*P1(2:end-1);
f = Fs/L*(0:(L/2));
figure
plot(f,P1) 
title("Single-Sided Amplitude Spectrum of X(t)")
xlabel("f (Hz)")
ylabel("|P1(f)|")