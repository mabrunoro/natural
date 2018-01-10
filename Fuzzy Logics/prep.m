function [treinamento,teste]=prep(datatable)

data = table2array(datatable);
minimal = min(data)
difference = max(data)-minimal;
atributos = []
for i=1:(length(data(1,:))-1)
    atributos = [atributos, (data(:,i)-minimal(i))/difference(i)];
end
atributos = [atributos, data(:,length(data(1,:)))]
% now I have atributos as normalized input matrix
% size of training matrix
streinamento = round(length(atributos(:,1))*0.7);
treinamento = []
teste = atributos;
for i=1:streinamento
    j = randi(length(teste(:,1)));
    treinamento = [treinamento;teste(j,:)];
    teste(j,:) = [];
% size of test matrix
end