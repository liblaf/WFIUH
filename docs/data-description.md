---
title: "数据说明"
---

青藏高原子流域来自全球流域数据集 HydroBASINS, sources: <https://www.hydrosheds.org/products/hydrobasins>

WFIUH 提取分为宽度函数 (WF) 提取与流速计算两个部分

1.  宽度函数提取自 SRTM 90m dem, sources: https://cmr.earthdata.nasa.gov/search/concepts/C1214622194-SCIOPS
2.  流速计算涉及坡度与土地利用数据
    坡度同样根据上述 dem 提取,
    土地利用数据为 10 m land cover products FROM-GLC（Finer Resolution Observation and Monitoring-Global Land Cover）
    ref: Peng Gong, Han Liu, Meinan Zhang, Li, C., Wang, J., & Huang, H. (2019). Stable classification with limited sample: Transferring a 30-m resolution sample set collected in 2015 to mapping 10-m resolution global land cover in 2017. Sci. Bull, 64, 370-373.

csv 文件中，flowTime 字段表示汇流时间, 间隔为 0.5h, frequency 表示 10mm 净雨量在该时段留到出口断面的流量比例
(后续如果选择方向二的同学在拟合分布的时候遇到无法与分布吻合的问题, 请跟我联系)
