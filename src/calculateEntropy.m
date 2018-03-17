function [entropy] = calculateEntropy(input, nbBins)
    [hdat, ~] = hist(input, nbBins);
    % hdat = hdat./sum(hdat);
    % entropy = -sum(hdat).*log2(hdat+eps);
    
    [~, m] = size(hdat);
    entropy = zeros(1,m);
    for column = 1:m
%         alphabet = unique(hdat(:,column));
%         frequency = zeros(size(alphabet));
%         for symbol = 1:length(alphabet)
%             frequency(symbol) = sum(hdat(:,column) == alphabet(symbol));
%         end
        P = hdat(:,column) / sum(hdat(:,column));
        entropy(column) = -sum(P .* log2(P+eps));
    end
end

