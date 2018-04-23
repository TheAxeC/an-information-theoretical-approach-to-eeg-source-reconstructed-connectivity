function [entropy] = calculateConditionalMI(input1, input2, input3, nbBins)
    entro1 = calculateConditionalEntropy(input1, input3, nbBins);
    entro2 = calculateConditionalEntropy(input2, input3, nbBins);
    entroJoint = calculateJointConditionalEntropy(input1, input2, input3, nbBins);
    entropy = entro1 + entro2 - entroJoint;
end