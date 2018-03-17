function [entropy] = calculateJointEntropy(input1, input2, nbBins)
    [~, m] = size(input1);
    entropy = zeros(1,m);
    for time = 1:m
        inp = [input1(:,time), input2(:,time)];
        [hdat, ~] = hist3(inp, [nbBins, nbBins]);
%         for column = 1:nbBins
%             alphabet = unique(hdat(:,column));
%             frequency = zeros(size(alphabet));
%             for symbol = 1:length(alphabet)
%                 frequency(symbol) = sum(hdat(:,column) == alphabet(symbol));
%             end
        P = hdat / sum(sum(hdat));
        entropy(time) = -sum(sum(P .* log2(P+eps)));
    end
end

