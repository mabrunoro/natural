function [err]=calcfuzzy(data,fis)

err=0;
for i = 1:size(data,1)
    e = round(evalfis(data(i,1:(size(data,2)-1)),fis));
    if(e ~= data(i,1:(size(data,2))))
        err = err + 1;
    end
end