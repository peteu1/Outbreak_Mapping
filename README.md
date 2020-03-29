# Outbreak_Mapping
Spatialtemporal visualization of COVID-19 spread in the United States


Data from: https://github.com/CSSEGISandData/COVID-19

Maps of US from: https://www.census.gov/cgi-bin/geo/shapefiles/index.php?year=2019&layergroup=States+%28and+equivalent%29


Other data sources:
https://raw.githubusercontent.com/beoutbreakprepared/nCoV2019/master/latest_data/outside_Hubei.data.19032020T011105.csv
https://raw.githubusercontent.com/jakobzhao/virus/master/assets/cases.csv

Existing maps:
https://www.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6
https://hgis.uw.edu/virus/
https://www.healthmap.org/covid-19/
http://www.vdh.virginia.gov/coronavirus/

Other sources:
https://www.wsls.com/health/2020/03/02/does-anyone-in-virginia-have-the-coronavirus-the-latest-from-the-health-department/


**To get started:**
* Set-up venv
  * python3 -m venv outbreak-env
  * source outbreak-env/bin/activate
  * pip install requirements.txt

**Commands:**
* bokeh serve --show Interactive_Map.ipynb  # To run the interactive map
