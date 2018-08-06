%% Loading data
load('../../../data/data-ai-thesis/FinalTimeSeries_Data.mat');

means = [];
for b = 1:9
    data_abs = Abstractness_TimeSeries(:,:,b);
    iqr_abs = iqr(data_abs);
    max_abs = max(data_abs);
    min_abs = min(data_abs);
    nbins = (max_abs - min_abs) ./ (2 * iqr_abs * 3404.^(-1/3));
    means = [means mean(nbins)];
end
mean(means)

data_abs = Concreteness_TimeSeries(:,:,1);
iqr_abs = iqr(data_abs);
max_abs = max(data_abs);
min_abs = min(data_abs);
nbins = (max_abs - min_abs) ./ (2 * iqr_abs * 3404.^(-1/3));
mean(nbins)

% calculateBins(data_abs, 10, 100);
