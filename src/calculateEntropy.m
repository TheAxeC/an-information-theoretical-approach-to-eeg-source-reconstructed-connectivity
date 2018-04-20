function [entropy] = calculateEntropy(input, nbBins)
    [hdat, ~] = hist(input, nbBins);
    
    [~, m] = size(hdat);
    entropy = zeros(1,m);
    for column = 1:m
        P = hdat(:,column) / sum(hdat(:,column));
        entropy(column) = -sum(P .* log2(P+eps));
    end
end

