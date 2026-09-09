function q60017140()
% Create data
t = 0:0.2:25;
x = sin(t);
y = tan(2*t);
z = sin(2*t);

% Create figure with points
hFig = figure('Position', [295,303,1014,626]); 
hAx = subplot(1,2,1,'Parent', hFig);
hLines = plot(hAx, t,x, t,y, t,z);

hAx(2) = subplot(1,2,2);

uicontrol('Parent', hFig, ...
  'Style', 'pushbutton',...
  'String', 'Get selected points index',...
  'Position', [5, 5, 200, 30],...
  'Units', 'pixels',...
  'Callback', {@brushCallback, hLines, hAx} ...
  );

brush(hFig, 'on');

end

function brushCallback(~, ~, hLines, hAx)
index_vec = cellfun(@logical, get(hLines,'BrushData'), 'UniformOutput', false);

plot(hAx(2), ...
  hLines(1).XData(index_vec{1}), hLines(1).YData(index_vec{1}), ...
  hLines(2).XData(index_vec{2}), hLines(2).YData(index_vec{2}), ...
  hLines(3).XData(index_vec{3}), hLines(3).YData(index_vec{3}));
end
