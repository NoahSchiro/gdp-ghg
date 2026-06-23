# Does GDP correlate with GHG emissions?

List available countries:
```
uv run main.py list
```

Plot a given country (optionally use log scale and optionally save it to a file):
```
uv run main.py plot -c <country> [--log] [--save file_path]
```

Sources for the data:
[GDP](https://data.imf.org/en/Data-Explorer?datasetUrn=IMF.RES:WEO(9.0.0))
[Emissions](https://edgar.jrc.ec.europa.eu/report_2024?vis=co2tot#data_download)

## Gallery
---

### China
![](images/china.png)
![](images/china_log.png)

### United States
![](images/united_states.png)
![](images/united_states_log.png)

### India
![](images/india.png)
![](images/india_log.png)
