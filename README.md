# An Information Theoretical Approach to EEG Source-Reconstructed Connectivity

Determining how distinct brain regions are connected and communicate with each other will shed light on how behaviour emerges [1]. In EEG studies, interpreting connectivity measures can be problematic, due to the high correlation between signals recorded from the scalp surface, a result of the volume conductance of the scalp and skin [2]. Therefore, meaningful connectivity patterns can be measured only from the from the spatiotemporal distribution of localised cortical sources, generally referred to as source reconstruction [3]. Still, spurious connectivity issues may persist in source reconstructed EEG data, rendering it vital to choose an appropriate measure of connectivity .

This thesis takes an information theoretical approach, which concerns model-free, probability based methods such as Conditional Mutual Information, Directed Information, and Directed feature information [4]. We will investigate how these measures are affected by volume conduction, using as ground truth connectivity between simulated cortical sources in the brainstorm toolbox [5]. In order to validate our methods further, these tools will also be compared with their statistical counterparts such as partial correlation, granger causality and dynamic causal modelling.

The student will start by studying state-of-the-art literature concerning source localisation and the problem of volume conduction. The student will also familiarise himself with information theoretical measures of brain connectivity. Afterwards, these measures will be applied to high density EEG datasets provided by the lab of computational neuroscience, but also to simulated source activity as a validation [2,6]. The novelty lies in the usage of these information theoretical algorithms for source-reconstructed activity.

## References

[1] Faes, Luca, et al. "Methodological advances in brain connectivity." Computational and mathematical methods in medicine 2012 (2012).

[2] Brunner, Clemens, et al. "Volume conduction influences scalp-based connectivity estimates." Frontiers in computational neuroscience 10 (2016).

[3] Grech, Roberta, et al. "Review on solving the inverse problem in EEG source analysis." Journal of neuroengineering and rehabilitation 5.1 (2008): 25.

[4] Ince, Robin AA, et al. "A statistical framework for neuroimaging data analysis based on mutual information estimated via a Gaussian copula." Human brain mapping 38.3 (2017): 1541-1573.

[5] Tadel, François, et al. "Brainstorm: a user-friendly application for MEG/EEG analysis." Computational intelligence and neuroscience2011 (2011): 8.

[6] Ghumare, Eshwar, et al. "Comparison of different Kalman filter approaches in deriving time varying connectivity from EEG data." Engineering in Medicine and Biology Society (EMBC), 2015 37th Annual International Conference of the IEEE. IEEE, 2015.

## Meeting

interaction information
    conditioning to find directed

collider/suppressor variable

h(x,y) > h(x) + h(y)

guassian caupula
    for few trials
Robin Ince

permutation significance

granger causality vs directed information
estimater = covariance matrix
    then linear granger

[4] Ince, Robin AA, et al. "A statistical framework for neuroimaging data analysis based on mutual information estimated via a Gaussian copula." Human brain mapping 38.3 (2017): 1541-1573.
