# Формулы для синтеза — инженерные выводы оркестратора

Эти формулы — собственная математическая запись и проектные правила. Сетевые основания для камерной модели и API поступят из агента 01. Сами по себе формулы не подтверждают качество на видео.

## Plane mapping and local sensitivity

Пусть H переводит undistorted image point (u,v,1) в homogeneous plane coordinates. Обозначим U=h11u+h12v+h13, V=h21u+h22v+h23, W=h31u+h32v+h33. Тогда X=U/W, Y=V/W при W≠0. Все клики, контрольные точки и детекции должны быть в одном пространстве undistorted pixels; normalize-to-camera-coordinates и undistort-to-newCameraMatrix — разные соглашения, их нельзя смешивать.

Jacobian J=d(X,Y)/d(u,v):

    J = (1/W) [[h11-X*h31, h12-X*h32],
               [h21-Y*h31, h22-Y*h32]]

Local first-order pixel uncertainty: Sigma_floor ≈ J Sigma_pixel J^T, conditional on fixed H. Это не учитывает uncertainty самой H, systematic footpoint bias, non-planarity и wrong ID. Их надо измерять/моделировать отдельно. Умножение H на скаляр не меняет X,Y: абсолютный |W| не является invariant численным критерием; используем normalized H, finite check и local sensitivity/validated support, а не произвольный универсальный порог W.

## Distance and time

d=||p1-p2||; velocity vector=(p(t2)-p(t1))/(t2-t1), units m and source seconds. ||velocity|| — скорость хорды между двумя наблюдениями, не длина реального пути и не label бег. Для d>0 и g=(p1-p2)/d:

    Var(d) ≈ g^T (Sigma1 + Sigma2 - Sigma12 - Sigma21) g

Cross covariances matter with shared calibration. При d≈0 linear distance approximation unreliable. Random errors, systematic bias и empirical percentile residuals нельзя называть одним confidence interval.

При независимых d и dt: Var(d/dt)≈Var(d)/dt²+d² Var(dt)/dt⁴. Для timestamp discontinuity/stale frame или identity discontinuity — invalid measurement, а не большое сглаживание.

## Boundary uncertainty and evidence state

Проектный вариант: signed distance s от точки к границе зоны положителен внутри. При обоснованном radial error budget e: s>e — inside; s<−e — outside; |s|≤e — ambiguous. Реальные e из hold-out/стратификации являются empirical quantiles, если нет доказательства верхней границы; условные статусы не гарантируют отсутствие ошибки.

Для d threshold r: при условно корректной границе error e, d_hat+e<r — уверенно ближе; d_hat-e>r — уверенно дальше; между ними — uncertainty. Operational warning policy может быть более консервативной и срабатывать при пересечении uncertainty envelope с опасной зоной; candidate предупреждение не обозначать подтверждённым физическим нарушением.

Event state proposal: unobservable → observed candidate → active → resolving → closed, with reset on stale/ID/camera-version discontinuity. Операционные причины (maintenance/authorized operation/machine inactive) — отдельный контекст, не геометрическая ошибка. Длительность считать в source seconds; дедупликация по camera/rule/track episode with documented ID-switch behavior. Состояние недостаточно данных — не safe.
