function [] = convertToJSON(loc_mat, name_mat, name_data, loc_json, name_json)
    data = load(strcat(loc_mat, name_mat));
    json = jsonencode(data.(name_data));
    fid = fopen(sprintf('%s%s%s', loc_json, name_json, '.json'),'wt');
    fprintf(fid, '%s', json);
    fclose(fid);
end
% function [] = visualizeGrouped(name, data, amount)
%     desktop = com.mathworks.mde.desk.MLDesktop.getInstance;
%     myGroup = desktop.addGroup(name);
%     desktop.setGroupDocked(name, 0);
%     myDim   = java.awt.Dimension(4, 2);   % 4 columns, 2 rows
%     % 1: Maximized, 2: Tiled, 3: Floating
%     desktop.setDocumentArrangement(name, 2, myDim)
%     figH    = gobjects(1, amount);
%     bakWarn = warning('off','MATLAB:HandleGraphics:ObsoletedProperty:JavaFrame');
%     for iFig = 1:amount
%        figH(iFig) = figure('WindowStyle', 'docked', ...
%           'Name', sprintf('Figure %d', iFig), 'NumberTitle', 'off');
%        drawnow;
%        pause(0.1);  % Magic, reduces rendering errors
%        set(get(handle(figH(iFig)), 'javaframe'), 'GroupName', name);
%        plot(data(:,:,iFig));
%     end
%     warning(bakWarn);
% end