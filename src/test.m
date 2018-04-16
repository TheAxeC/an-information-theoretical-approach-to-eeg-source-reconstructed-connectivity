%% Loading data
load('../data/source-localization/Data.mat');

LT = AbstractnessScouts(1).Vertices;
LPF = AbstractnessScouts(2).Vertices;
RP = AbstractnessScouts(3).Vertices;
RT1 = AbstractnessScouts(4).Vertices;
RT2 = AbstractnessScouts(5).Vertices;
RPF = AbstractnessScouts(6).Vertices;

LT_data_abs = Abstract_Averaged.ImageGridAmp(LT,:);
LPF_data_abs = Abstract_Averaged.ImageGridAmp(LPF,:);
RP_data_abs = Abstract_Averaged.ImageGridAmp(RP,:);
RT1_data_abs = Abstract_Averaged.ImageGridAmp(RT1,:);
RT2_data_abs = Abstract_Averaged.ImageGridAmp(RT2,:);
RPF_data_abs = Abstract_Averaged.ImageGridAmp(RPF,:);

LT_data_con = Concrete_Averaged.ImageGridAmp(LT,:);
LPF_data_con = Concrete_Averaged.ImageGridAmp(LPF,:);
RP_data_con = Concrete_Averaged.ImageGridAmp(RP,:);
RT1_data_con = Concrete_Averaged.ImageGridAmp(RT1,:);
RT2_data_con = Concrete_Averaged.ImageGridAmp(RT2,:);
RPF_data_con = Concrete_Averaged.ImageGridAmp(RPF,:);

nb_bins = 200;
LT_mi = calculateMutualInformation(LT_data_abs, LT_data_con, nb_bins);
LPF_mi = calculateMutualInformation(LPF_data_abs, LPF_data_con, nb_bins);
RP_mi = calculateMutualInformation(RP_data_abs, RP_data_con, nb_bins);
RT1_mi = calculateMutualInformation(RT1_data_abs, RT1_data_con, nb_bins);
RT2_mi = calculateMutualInformation(RT2_data_abs, RT2_data_con, nb_bins);
RPF_mi = calculateMutualInformation(RPF_data_abs, RPF_data_con, nb_bins);

%% Experiments

r2_a = randi(15000,42,1);
r2_abs = Abstract_Averaged.ImageGridAmp(r2_a,:);
r2_c = randi(15000,42,1);
r2_con = Concrete_Averaged.ImageGridAmp(r2_c,:);

% r2_abs = randi(42,550);
% r2_con = randi(42,550);
% tmp_mi = calculateMutualInformation(LT_data_con, LT_data_con, nb_bins);
LT_mi_self = calculateMutualInformation(LT_data_abs, LT_data_abs, nb_bins);
LT_mi_self_con = calculateMutualInformation(LT_data_con, LT_data_con, nb_bins);
r2_mi = calculateMutualInformation(r2_abs, r2_con, nb_bins);
% r2_mi_test = calculateMutualInformation(r2_abs, LT_data_con, nb_bins);
% r2_mi_test_2 = calculateMutualInformation(LT_data_con, r2_con, nb_bins);
% figure;
% plot(LT_mi)
% figure;
% plot(r2_mi)
% figure;
% plot(LT_mi_self)
% figure;
% plot(LT_mi_self_con)

LT_mi_self = calculateMutualInformation(LT_data_abs, LT_data_abs, nb_bins);
LT_mi_self2 = calculateEntropy(LT_data_abs, nb_bins) - calculateConditional(LT_data_abs, LT_data_abs, nb_bins);
LT_mi_self3 = calculateEntropy(LT_data_abs, nb_bins);
figure;
hold on;
plot(LT_mi_self)
plot(LT_mi_self2)
plot(LT_mi_self3)
hold off;
% figure;
% plot(LT_mi_self)

% calculateBins(LT_data_abs, 20, 20);

%% Find index with highest average activity
% tmp = zeros(550, 1);
% for i = 1:550
%    tmp(i) =  mean(LT_data_abs(:,i));
% end
% [M,I] = max(tmp)
