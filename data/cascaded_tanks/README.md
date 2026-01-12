The cascaded tanks experiment requires external data.
Make sure this folder contains the file `dataBenchmark.mat` from [Schoukens et al.](https://data.4tu.nl/articles/_/12960104).

Download and extract (run from repo root):
```bash
curl -L -o /tmp/cascaded_tanks.zip https://data.4tu.nl/ndownloader/items/d4810b78-6cdd-48fe-8950-9bd601e5f47f/versions/1
unzip -p /tmp/cascaded_tanks.zip CascadedTanksFiles.zip > /tmp/CascadedTanksFiles.zip
unzip -p /tmp/CascadedTanksFiles.zip CascadedTanksFiles/dataBenchmark.mat > data/cascaded_tanks/dataBenchmark.mat
```

Checksum (SHA256):
`cb2f88d4388be4d3f2a24c6402fba804976aac5f2e1f26cda59ea0a38d016eab`
