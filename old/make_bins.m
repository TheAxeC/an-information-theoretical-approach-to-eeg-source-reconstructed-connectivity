function [result] = make_bins(input, bin_size, min_val, max_val)
%MAKE_BINS
%   Convert an input array (sampled in time) into a binned discrete array
%   [a;a;b;a] is converted into P(a)=3/4  P(b)=1/4
    size = length(input);
    result = zeros(1, floor(((max_val - min_val) / bin_size) + 1));
    for k=1:2
        ind = floor((input(k) - min_val) / bin_size);
        result(ind) = result(ind) + 1; 
    end
    result = result / size;
end

