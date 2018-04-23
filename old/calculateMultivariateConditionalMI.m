function [entropy] = calculateMultivariateConditionalMI(nbBins, cond, varargin)
    amount = nargin - 1;
    if amount == 1
        entropy = calculateEntropy(varargin{1}, nbBins);
    elseif amount == 2
        entropy = calculateMultivariate(nbBins, varargin) - calculateMultivariateConditional(nbBins, varargin, varargin);
    else
        entropy = calculateEntropy(input1, nbBins) - calculateMutualInformation(input1, input2, nbBins);
    end
end