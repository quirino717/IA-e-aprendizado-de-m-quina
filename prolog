male(jose).
male(joao).
male(paulo).
male(carlos).

female(maria).
female(ana).
female(helena).
female(joana).

casal(jose,maria).
casal(paulo,helena).

progenitor(jose,joao).
progenitor(maria,joao).
progenitor(jose,ana).
progenitor(maria,ana).

progenitor(joao,paulo).

progenitor(ana,helena).
progenitor(ana,joana).

progenitor(paulo,carlos).
progenitor(helena,carlos).

% X é irmã de Y
irma(X,Y):-female(X),progenitor(Z,X),progenitor(Z,Y),not(X=Y).
% X é irmão de Y
irmao(X,Y):-male(X),progenitor(Z,X),progenitor(Z,Y),not(X=Y).

% X é descendente de Y
descendente(X,Y):-progenitor(Y,X);(progenitor(Y,Z),progenitor(Z,X));(progenitor(Y,W),progenitor(W,Z),progenitor(Z,X)).

% X é a mãe de Y
mae(X,Y):-female(X),progenitor(X,Y),not(X=Y).
% X é o pai de Y
pai(X,Y):-male(X),progenitor(X,Y),not(X=Y).

% X é o vô de Y
avô(X,Y):-pai(X,Z),progenitor(Z,Y),not(X=Y).
% X é a vó de Y
avó(X,Y):-mae(X,Z),progenitor(Z,Y),not(X=Y).

% X é o bisavô de Y
biso(X,Y):-pai(X,Z),avô(Z,Y),not(X=Y).
% X é a bisavó de Y
bisa(X,Y):-mae(X,Z),avó(Z,Y),not(X=Y).

% X é o tio de Y
tio(X,Y):-irmao(X,Z),progenitor(Z,Y),not(X=Y).
% X é a tia de Y
tia(X,Y):-irma(X,Z),progenitor(Z,Y),not(X=Y).

% X é primo de Y
primo(X,Y):-male(X),(tio(Z,X);tia(Z,X)),progenitor(Z,Y).
% X é prima de Y
prima(X,Y):-female(X),(tio(Z,X);tia(Z,X)),progenitor(Z,Y).