function [mi] = calculateMutualInformation(input1, input2, nbBins)
    entro1 = calculateEntropy(input1, nbBins);
    entro2 = calculateEntropy(input2, nbBins);
    entroJoint = calculateJointEntropy(input1, input2, nbBins);
    mi = entro1 + entro2 - entroJoint;
end