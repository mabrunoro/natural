function [err]=calcfuzzy(treinamento,fis)

err=0;
for i = 1:size(treinamento,1)
    e = round(evalfis(treinamento(i,1:(size(treinamento,2)-1)),fis));
    if e ~= treinamento(i,1:(size(treinamento,2)))
        err = err + 1;
        disp([i,evalfis(treinamento(i,1:(size(treinamento,2)-1)),fis),treinamento(i,(size(treinamento,2)))])
    end
end

err = err/size(treinamento,1);