function [entropy] = calculateJointConditionalEntropy(input1, input2, input3, nbBins)
    % H(input1, input2 | input3)
    [~, m] = size(input1);
    entropy = zeros(1,m);
    for time = 1:m
        inp = [input1(:,time), input2(:,time)];
        [hdat, ~] = hist3(inp, [nbBins, nbBins]);
        P = hdat / sum(sum(hdat));
        entropy(time) = -sum(sum(P .* log2(P+eps)));
    end
end