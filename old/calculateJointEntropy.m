function [entropy] = calculateJointEntropy(input1, input2, nbBins)
    [~, m] = size(input1);
    entropy = zeros(1,m);
    for time = 1:m
        i1 = input1(:,time);
        i2 = input2(:,time);
        inp = [i1 i2];
        [hdat, ~] = hist3(inp, [nbBins, nbBins]);
        P = hdat / sum(sum(hdat));
        entropy(time) = -sum(sum(P .* log2(P+eps)));
    end
end

