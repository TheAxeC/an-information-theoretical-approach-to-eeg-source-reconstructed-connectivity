function [entropy] = calculateConditional(input1, input2, nbBins)
    entropy = calculateEntropy(input1, nbBins) - calculateMutualInformation(input1, input2, nbBins);
end