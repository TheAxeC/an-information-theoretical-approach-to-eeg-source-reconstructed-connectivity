function [entropy] = calculateMultivariateMI(nbBins, varargin)
    amount = nargin - 1;
    if amount == 2
        entropy = calculateMutualInformation(varargin{1}, varargin{2}, nbBins);
    else 
        last = 1
        entropy = calculateMultivariate(nbBins, varargin) - calculateMultivariateConditional(nbBins, last, varargin);
    end
end