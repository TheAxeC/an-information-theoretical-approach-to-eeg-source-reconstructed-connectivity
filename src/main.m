%% Loading data
full = load('../../../../../Documents/data-ai-thesis/FinalTimeSeries_Data.mat');
rest = load('../../../../../Documents/data-ai-thesis/RSFinalTimeSeries_Alldata.mat');

% visualizeGrouped('Abstractness_TimeSeries', Abstractness_TimeSeries, 9);
% visualizeGrouped('CommonAbstractness_TimeSeries', CommonAbstractness_TimeSeries, 4);
% visualizeGrouped('CommonConcreteness_TimeSeries', CommonConcreteness_TimeSeries, 4);
% visualizeGrouped('Concreteness_TimeSeries', Concreteness_TimeSeries, 8);

% loc = '../../../../../Documents/data-ai-thesis/';
% convertToJSON('Abstractness_TimeSeries', full.Abstractness_TimeSeries, loc);
% convertToJSON('CommonAbstractness_TimeSeries', full.CommonAbstractness_TimeSeries, loc);
% convertToJSON('CommonConcreteness_TimeSeries', full.CommonConcreteness_TimeSeries, loc);
% convertToJSON('Concreteness_TimeSeries', full.Concreteness_TimeSeries, loc);
% convertToJSON('Abstractness_TimeSeries_rest', rest.Abstractness_TimeSeries, loc);
% convertToJSON('Common_TimeSeries_rest', rest.Common_TimeSeries, loc);
% convertToJSON('Concreteness_TimeSeries_rest', rest.Concreteness_TimeSeries, loc);

function [] = visualizeGrouped(name, data, amount)
    desktop = com.mathworks.mde.desk.MLDesktop.getInstance;
    myGroup = desktop.addGroup(name);
    desktop.setGroupDocked(name, 0);
    myDim   = java.awt.Dimension(4, 2);   % 4 columns, 2 rows
    % 1: Maximized, 2: Tiled, 3: Floating
    desktop.setDocumentArrangement(name, 2, myDim)
    figH    = gobjects(1, amount);
    bakWarn = warning('off','MATLAB:HandleGraphics:ObsoletedProperty:JavaFrame');
    for iFig = 1:amount
       figH(iFig) = figure('WindowStyle', 'docked', ...
          'Name', sprintf('Figure %d', iFig), 'NumberTitle', 'off');
       drawnow;
       pause(0.1);  % Magic, reduces rendering errors
       set(get(handle(figH(iFig)), 'javaframe'), 'GroupName', name);
       plot(data(:,:,iFig));
    end
    warning(bakWarn);
end

function [] = convertToJSON(name, data, loc)
    json = jsonencode(data);
    fid = fopen(sprintf('%s%s%s', loc, name, '.json'),'wt');
    fprintf(fid, '%s', json);
    fclose(fid);
end