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

mean(LT_mi)
% mean(LPF_mi)
% mean(RP_mi)
% mean(RT1_mi)
% mean(RT2_mi)
% mean(RPF_mi)

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
% mean(tmp_mi)
% mean(r2_mi)
% mean(r2_mi_test)
% mean(r2_mi_test_2)
figure;
plot(LT_mi)
figure;
plot(r2_mi)
figure;
plot(LT_mi_self)
figure;
plot(LT_mi_self_con)

entro1 = calculateEntropy(LT_data_abs, nb_bins);
figure;
plot(entro1)
% IGNORING TIME

% bin_size = 1e-10;
% [min_val_abs, I] = min(Abstract_Averaged.ImageGridAmp(:));
% [max_val_abs, I] = max(Abstract_Averaged.ImageGridAmp(:));
% [min_val_con, I] = min(Concrete_Averaged.ImageGridAmp(:));
% [max_val_con, I] = max(Concrete_Averaged.ImageGridAmp(:));
% min_val = min(min_val_abs, min_val_con);
% max_val = max(max_val_abs, max_val_con);
% size = floor(((max_val - min_val) / bin_size) + 1);
% 
% % todo
% %   put binning into separate function
% %   rewrite MI/Entropy/JointEntropy functions
% %   make slides
% 
% binnedA = make_bins(LT_data_abs(1,:), bin_size, min_val, max_val);
% binnedB = make_bins(LT_data_abs(2,:), bin_size, min_val, max_val);
% binnedC = make_bins(LT_data_con(1,:), bin_size, min_val, max_val);
% binnedD = make_bins(LT_data_con(2,:), bin_size, min_val, max_val);
% 
% MI = MutualInformation(binnedA', binnedA');
% MI = MutualInformation(binnedA', binnedB');
% MI = MutualInformation(binnedA', binnedC');
% MI = MutualInformation(binnedA', binnedD');
% MI = MutualInformation(binnedB', binnedB');
% MI = MutualInformation(binnedB', binnedC');
% MI = MutualInformation(binnedB', binnedD');