function [entropy] = calculateConditionalEntropy(input1, input2, nbBins)
    entro2 = calculateEntropy(input2, nbBins);
    entroJoint = calculateJointEntropy(input1, input2, nbBins);
    entropy = entroJoint - entro2;
end