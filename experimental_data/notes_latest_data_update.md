- Changes in last data update
  - Use substracted column for antiparallel accumulation -> no simulation parameter affected
  - minor changes in 1nM single microtubules -> no simulation parameter affected
  - Different equilibrium densities (corrected)
    - What I was using was
        ```
        isolated 1nM 0.01165 < density isolated (1nM)
        isolated 6nM 0.19992 < density isolated (6nM)
        antiparallel 1nM 0.19086 < density antiparallel bundle
        parallel 1nM 0.07323 < density parallel bundle
        ```
    - Now I am using
        ```
        isolated 1nM 0.01165 < same
        isolated 6nM 0.19992 < same
        antiparallel 1nM 0.1729 < changed to "density antiparallel overlap"
        parallel 1nM 0.05531 < changed to "density parallel overlap"
        ```
    - This required re-running the simulations in `runs_overlaps_*`
