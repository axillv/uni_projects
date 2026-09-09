%%% Part B %%%
clear;
clc;
load source.mat
% Here you can change t=t(1:5000) etc.
%t=t(15001:20000);
%% Calculations
y_errors = num2cell(zeros(3,6));

encoded_p5 = {0, 0, 0};
encoded_p10 = {0, 0, 0};
a_coeff_p5 = {0, 0, 0};
a_coeff_p10 = {0, 0, 0};
decoded_p5 = {0, 0, 0};
decoded_p10 = {0, 0, 0};

msqerrors = num2cell(zeros(3,6));

for N=1:3
    for p=5:10
        % Calculate encoded signals, coefficients and y errors.
        if p ~=5 && p ~= 10
            [~, ~, y_errors{N, p-4}] = dpcm_encode(t, p, N,-3.5, 3.5);
        end

        if p == 5
            [encoded_p5{N}, a_coeff_p5{N}, y_errors{N, p-4}] = dpcm_encode(t, p, N,-3.5, 3.5);
        end
        
        if p == 10
            [encoded_p10{N}, a_coeff_p10{N}, y_errors{N, p-4}] = dpcm_encode(t, p, N,-3.5, 3.5);
        end

        % Calculate mean square errors y.
        msqerrors{N,p-4} = sumsqr(y_errors{N,p-4})/numel(y_errors{N,p-4});
    end
end

for N=1:3
    decoded_p5{N} = dpcm_decode(encoded_p5{N}, a_coeff_p5{N});
    decoded_p10{N} = dpcm_decode([encoded_p10{N}], a_coeff_p10{N});
end

%% Question 2
%Plot for p = 5
figure
hold on
plot(t, 'c')
plot(y_errors{1,1}, 'r-')
plot(y_errors{2,1}, 'g-')
plot(y_errors{3,1}, 'b-')
hold off
title("y prediction error for p=5, N=1,2,3")
legend('Signal', 'N=1', 'N=2', 'N=3')
xlabel('Sample')
ylabel('y prediction error')

%Plot for p = 10
figure
hold on
plot(t, 'c')
plot(y_errors{1,6}, 'r-')
plot(y_errors{2,6}, 'g-')
plot(y_errors{3,6}, 'b-')
hold off
title("y prediction error for p=10, N=1,2,3")
legend('Signal', 'N=1', 'N=2', 'N=3')
xlabel('Sample')
ylabel('y prediction error')

%% Question 3
figure
hold on
bar(5:10, cell2mat(msqerrors)')
legend('N=1', 'N=2', 'N=3')
xlabel('p values')
ylabel('mean-squared error y')
hold off

%% Question 4
%Plots for p = 5
figure
hold on
plot(t, 'c')
plot(decoded_p5{1}, 'r-')
plot(decoded_p5{2}, 'g-')
plot(decoded_p5{3}, 'b-')
hold off
title("Recreated signal for p=5, N=1,2,3")
legend('Signal', 'N=1', 'N=2', 'N=3')
xlabel('Sample')
ylabel('value')

figure
hold on

plot(t, 'c')
plot(t - decoded_p5{1}, 'r-')
plot(t - decoded_p5{2}, 'g-')
plot(t - decoded_p5{3}, 'b-')
hold off
title("Original minus recreated signal for p=5, N=1,2,3")
legend('Signal', 'N=1', 'N=2', 'N=3')
xlabel('Sample')
ylabel('value')

%Plots for p = 10
figure
hold on
plot(t, 'c')
plot(decoded_p10{1}, 'r-')
plot(decoded_p10{2}, 'g-')
plot(decoded_p10{3}, 'b-')
hold off
title("Recreated signal for p=10, N=1,2,3")
legend('Signal', 'N=1', 'N=2', 'N=3')
xlabel('Sample')
ylabel('value')

figure
hold on
plot(t, 'c')
plot(t - decoded_p10{1}, 'r-')
plot(t - decoded_p10{2}, 'g-')
plot(t - decoded_p10{3}, 'b-')
hold off
title("Original minus recreated signal for p=10, N=1,2,3")
legend('Signal', 'N=1', 'N=2', 'N=3')
xlabel('Sample')
ylabel('value')

%% DPCM Encoding %%
function [enc_signal, a_coeff_quant, y_error] = dpcm_encode(signal, p, N, min_val, max_val)
    % Calculate a coefficients based on the input signal
    auto_corr = xcorr(signal, p, 'unbiased');
    R = toeplitz(auto_corr(p+1:end-1));
    r = auto_corr(p+2:end);

    a_coeff = R\r;

    % Alternative: Levinson way (requires multiplying the final array with -1!!)
    %a_coeff = levinson(auto_corr(p+1:end), p);
    %a_coeff = a_coeff(2:end); % Drop a(0)
  
    % Convert the indices into the actual values for the coefficients a
    a_coeff_indices = arrayfun(@(x) my_quantizer(x, 8, -2, 2), a_coeff);

    % Calculate the quantizing centers
    %delta = (max_value - min_value) / (2^N);
    %centers = (max_value - delta/2):-delta:(min_value + delta/2);
    delta_center_coeff = (2 - (-2)) / (2^8);
    centers_coeff = (2 - delta_center_coeff/2):-delta_center_coeff:(-2 + delta_center_coeff/2);
    
    a_coeff_quant = centers_coeff(a_coeff_indices);
    
    % Initialize arrays
    enc_signal = zeros(size(signal));
    memory = zeros(p, 1);

    % Calculate the quantizer centers
    delta = (max_val - min_val) / (2^N);
    centers = (max_val - delta/2):-delta:(min_val + delta/2);

    y_error = zeros(size(signal)); % So it's plotable

    for n=1:length(signal)
        % Predict y
        y_predicted = a_coeff_quant * memory;
        y_error(n) = signal(n) - y_predicted; 

        % Calc y_quant
        y_quant_ind = my_quantizer(y_error(n), N, min_val, max_val); 
        
        y_quant = centers(y_quant_ind);
        enc_signal(n) = y_quant; 

        % update memory
        y_new_memory = y_quant + y_predicted;
        memory = [y_new_memory; memory(1:end-1)];

    end

end

%% DPCM Decoding %%
function [dec_signal] = dpcm_decode(enc_signal, a_coeff_quant)
    % Initialize arrays
    dec_signal = zeros(size(enc_signal));
    memory = zeros(numel(a_coeff_quant), 1);

    for n=1:length(enc_signal)
        % Reconstruct signal
        y_predicted = a_coeff_quant * memory;
        y = enc_signal(n) + y_predicted; 
        dec_signal(n) = y;
        
        % update memory
        memory = [y; memory(1:end-1)];

    end

end

%% Quantizer %%
function index = my_quantizer(value, N, min_value, max_value)
    % Calculate delta and find the centers
    delta = (max_value - min_value) / (2^N);
    centers = (max_value - delta/2):-delta:(min_value + delta/2);
    
    % Find the difference between quantized values and input value
    differences = abs(centers - value);

    % Find quantized value with minimum distance from input value
    [~, index] = min(differences);
end

