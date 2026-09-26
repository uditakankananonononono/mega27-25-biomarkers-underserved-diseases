# 6b. Numbered formulas (program gate: 10+)
(1) log2 CPM: x_ij' = log2( x_ij / sum_k(x_kj) * 10^6 + 1 )
(2) Kruskal-Wallis H: H = 12/(N(N+1)) * sum_g( R_g^2/n_g ) - 3(N+1)
(3) Benjamini-Hochberg FDR: q_(i) = p_(i) * m / i (step-up, monotone)
(4) Effect size: d = median(x'_severe) - median(x'_mild); gate |d| >= 0.5
(5) Ordinal concordance index: c = #{(i,j): sign(s_i-s_j)=sign(y_i-y_j)} /
     #{(i,j): y_i != y_j}
(6) Immediate-threshold ordinal model: P(y >= k | x) = sigma(a_k + b'x),
     score s = 1 + sum_k P(y >= k | x)
(7) Cox & Snell R2: R2 = 1 - exp( -2/n * (LL_1 - LL_0) )
(8) Elastic-net objective: min_b [ -LL(b)/n + lambda( alpha||b||_1 +
     (1-alpha)||b||_2^2/2 ) ], alpha = 0.5
(9) Direction-predicted enrichment p: p = (1 + #{b: f_b >= f_obs}) / 10001,
     f over 10,000 size-preserving random gene sets
(10) Severity module score: S_j = sum_m( w_m * z(x'_mj) ), w_m = sign(d_m),
     z = per-gene standardization over samples
(11) Bootstrap CI of delta c-index: delta = c_model - c_bench over B=1000
     resamples; beat requires the 95% percentile interval to exclude 0.
