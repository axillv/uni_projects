%TODO: Sxoliasmos 1b, 2b, ++?
%%% Part A %%%
clear;
clc;

%% Question 1.a 
image = imread('parrot.png');
[symbol_counts, symbols] = groupcounts(image(:));
probabilities = symbol_counts./numel(image);

disp('1.a) Probabilities: ');
disp(table(probabilities, symbols));

%% Question 1.b
huff_dict = huffmandict(symbols, probabilities);
entropy = -sum(arrayfun(@(x) x*log2(x), probabilities));

dict_lengths = cellfun('length', huff_dict(:,2));
average_length = sum(probabilities .* dict_lengths);

efficiency = entropy/average_length;

disp(['1.b.i) Entropy: ' num2str(entropy)]);
disp(['1.b.ii) Average Length: ' num2str(average_length)]);
disp(['1.b.iii) Efficiency: ' num2str(efficiency)]);

%% Question 2.a
pairs = image(:);
pairs = [pairs(1:2:end), pairs(2:2:end)];

[pair_symbol_counts, pair_symbols] = groupcounts(pairs);
pair_probabilities = pair_symbol_counts./(numel(pairs)/2);
pair_symbols = [pair_symbols{1}, pair_symbols{2}];

disp('2.a) Probabilities: ');
disp(table(pair_probabilities, pair_symbols));

%% Question 2.b
% We need to convert pair_symbols to cell (178x1)
huff_dict_2nd = huffmandict(num2cell(pair_symbols, 2), pair_probabilities);
entropy_2nd = -sum(arrayfun(@(x) x*log2(x), pair_probabilities));

dict_lengths_2nd = cellfun('length', huff_dict_2nd(:,2));
average_length_2nd = sum(pair_probabilities .* dict_lengths_2nd);

efficiency_2nd = entropy_2nd/average_length_2nd;

disp(['1.b.i) Entropy: ' num2str(entropy_2nd)]);
disp(['1.b.ii) Average Length: ' num2str(average_length_2nd)]);
disp(['1.b.iii) Efficiency: ' num2str(efficiency_2nd)]);

%% Question 3.a
disp(['3.a) H(X²) = ' num2str(entropy_2nd) ' < 2H(X) = 2 × ' num2str(entropy)])

%% Question 3.b
disp('3.b)')
disp(['For 1st order, entropy: ' num2str(entropy) ' < L=' num2str(average_length) ' < ' num2str(entropy+1)])
disp(['For 2nd order, entropy: ' num2str(entropy_2nd) ' < L=' num2str(average_length_2nd) ' < ' num2str(entropy_2nd+1)])

%% Question 4
encoded_image = huffmanenco(image(:), huff_dict);

decoded_image = huffmandeco(encoded_image, huff_dict);
decoded_image = reshape(decoded_image, 200, []);
total_error = sumabs(image - decoded_image);

bI = reshape((dec2bin(typecast(image(:),'uint8'),4)-'0').',1,[]);
J_ratio = numel(encoded_image) / numel(bI); 

disp(['4) Total error in decoded image = ' num2str(total_error)])
disp(['J = ' num2str(J_ratio)])

%% Question 5
% test the channel
TEST_TRANSMISSIONS = 1000;
transmission_errors = 0;
for i = 1:TEST_TRANSMISSIONS
    transmitted_image = binary_symmetric_channel(encoded_image);
    temp_errors = sum(transmitted_image ~= encoded_image);
    transmission_errors = transmission_errors + temp_errors;
end
p = transmission_errors / (numel(encoded_image) * TEST_TRANSMISSIONS);

% Calculations for input X
encoded_occurances = groupcounts(encoded_image);
encoded_probabilities = encoded_occurances./numel(encoded_image);

% Joint and conditional calculations
joint_probabilities = [encoded_probabilities .* [1-p; p] ...
                       encoded_probabilities .* [p; 1-p]];

Y_given_X_entropy = -sum(joint_probabilities .* log2([1-p, p; p, 1-p]), "all");

% Calculation for output Y
channel_probabilities = [joint_probabilities(1,1) + joint_probabilities(1,2);
                         joint_probabilities(2,1) + joint_probabilities(2,2)];

channel_entropy =  -sum(arrayfun(@(x) x*log2(x), channel_probabilities));

% Calculate entropy Hb and capacity
Hb = -p*log2(p) - (1-p)*log2(1-p);
capacity = 1 - Hb;
mutual_information = channel_entropy - Y_given_X_entropy;

fprintf('5) p=%.2f, capacity=%f bits, mutual information = %f bits', p, capacity, mutual_information)

%% Clear utility variables
clear symbol_counts dict_lengths;               % Q1
clear pair_symbol_counts dict_lengths_2nd;      % Q2
clear temp_errors;                              % Q5
