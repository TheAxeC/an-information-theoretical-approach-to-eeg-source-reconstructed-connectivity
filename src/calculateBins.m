function [] = calculateBins(input, max, steps)
    figure;
    hold on
    legendInfo = strings(max,1);
    for b = 1:max
        bins = b * steps;
        tmp = calculateEntropy(input, bins);
        legendInfo(b) = ['nbBins = ' num2str(bins)];
        plot(tmp)
    end
    legend(legendInfo);
    hold off
end

