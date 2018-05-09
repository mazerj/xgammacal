function showcalib(fname)
%function showcalib(fname)
%
% Plot the results from the Monaco Optix Calibration program for
% gamma and color calibration of CRT and LCD displays. Generates
% a nice plot and prints the R, G, B and LUM gamma values on the
% console.
%
% INPUT:
%   f = filename containing calibration results
%
% OUTPUT:
%   none
%

d=importdata(fname);
d=d.data;

n = 1;
r=d(:,n); n=n+1;
g=d(:,n); n=n+1;
b=d(:,n); n=n+1;
Y=d(:,n); n=n+1;
x=d(:,n); n=n+1;
y=d(:,n); n=n+1;

subplot(4,4,[1:8]);
cla; hold on;

G = [];
gain = [];

ix = (r & g & b);
plot(r(ix), Y(ix), 'ko');
f = fit(r(ix), Y(ix), ...
        fittype('(alpha .* (x .^ gamma)) + beta'), ...
        'StartPoint', [1.0 0.0 2.4]);
plot(f, 'k-');
G = [G f.gamma];
gain = [gain feval(f, 255)];

ix = (r & ~g & ~b);
plot(r(ix), Y(ix), 'ro');
f = fit(r(ix), Y(ix), ...
        fittype('(alpha .* (x .^ gamma)) + beta'), ...
        'StartPoint', [1.0 0.0 2.4]);
plot(f, 'r-');
G = [G f.gamma];
gain = [gain feval(f, 255)];


ix = (~r & g & ~b);
plot(g(ix), Y(ix), 'go');
f = fit(g(ix), Y(ix), ...
        fittype('(alpha .* (x .^ gamma)) + beta'), ...
        'StartPoint', [1.0 0.0 2.4]);
plot(f, 'g-');
G = [G f.gamma];
gain = [gain feval(f, 255)];

ix = (~r & ~g & b);
plot(b(ix), Y(ix), 'bo');
f = fit(b(ix), Y(ix), ...
        fittype('(alpha .* (x .^ gamma)) + beta'), ...
        'StartPoint', [1.0 0.0 2.4]);
plot(f, 'b-');
G = [G f.gamma];
gain = [gain feval(f, 255)];

fprintf('  lum gamma = %.2f\n', G(1));
fprintf('  red gamma = %.2f\n', G(2));
fprintf('green gamma = %.2f\n', G(3));
fprintf(' blue gamma = %.2f\n', G(4));

ylabel('big Y');
xlabel('gun setting');
legend('k', 'k', 'r', 'r', 'g', 'g', 'b', 'b', 'location', 'northwest');
hold off;
title(sprintf('%s: lum gamma=%.2f', fname, G(1)));

subplot(4,4,[9 10 13 14]);
plot(x, y, 'k.');
hold on;
a = find(x == max(x));
b = find(y == max(y));
plot([x(a(1)) x(b(1))], [y(a(1)) y(b(1))], 'k-');
a = find(x == max(x));
b = find(y == min(y));
plot([x(a(1)) x(b(1))], [y(a(1)) y(b(1))], 'k-');
a = find(y == max(y));
b = find(y == min(y));
plot([x(a(1)) x(b(1))], [y(a(1)) y(b(1))], 'k-');
hold off;


axis square
xlabel('CIE x');
ylabel('CIE y');
title('monitor gamut');

subplot(4,4,[11 12 15 16]);
cla;
text(0,.5,sprintf('L = %.2f\nR = %.2f\nG = %.2f\nB = %.2f\n', G))
axis off

