%% create the challenge
clc;clear
%% open the original file
[y,Fs] = audioread('original file.mp3');
y = y(1:Fs*11);
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

%% create the database
% start time: 8 november 2024 00:00
% 1731006000 unix epoc time
T1 = convertTo(datetime(2024,11,08,00,00,00),'posixtime');
freqData = 50 + sin( 2*pi/(8640*2) * (1:1:(8640*2)) )';

%% create the sine wave
sinF = freqData(10623);
sinewave = 0.02*sin(2*pi*sinF * (0:(1/Fs):(11)) );
% check its FFT
L = length(sinewave);
Y = fft(sinewave);
P2 = abs(Y/L);
P1 = P2(1:L/2+1);
P1(2:end-1) = 2*P1(2:end-1);
f = Fs/L*(0:(L/2));
figure
plot(f,P1) 
title("Single-Sided Amplitude Spectrum of X(t)")
xlabel("f (Hz)")
ylabel("|P1(f)|")


%% create new music
newdata = y + sinewave(2:end);
% optionally take FFT again
L = length(newdata);
Y = fft(newdata);
P2 = abs(Y/L);
P1 = P2(1:L/2+1);
P1(2:end-1) = 2*P1(2:end-1);
f = Fs/L*(0:(L/2));
figure
plot(f,P1) 
title("Single-Sided Amplitude Spectrum of X(t)")
xlabel("f (Hz)")
ylabel("|P1(f)|")

%% flag is ictf{1731129360}, situated at 10537, for frequency 49.3636
% this is different from {1731130220} 10623 for frequency 49.3398