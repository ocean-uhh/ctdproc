# ctdproc

Processes raw Sea-Bird SBE 911plus CTD data: `.hex`/`.XMLCON` in,
calibration-corrected `.cnv` out. Works on any cruise's hex/XMLCON pair
(sensor setup is detected from the XMLCON itself) - `name:`/`ind:` in the
config just pick the cast. Output feeds into [`caldip`](../caldip) for the
calibration-dip stats.

---

## Layout

```text
├── src/
│   ├── ctdproc/                # main.py + the 3 finders below
│   └── seabirdscientific/      # vendored Sea-Bird toolkit, v3.1.2
├── tests/                      # pytest regression suite
├── proc/                       # working directory: configs + pipeline output
├── pyproject.toml / requirements.txt / environment.yml
└── README.md
```

`seabirdscientific/` is vendored, not pip-installed (see Known gaps).

---

## Install

```bash
pip install -r requirements.txt && pip install -e .
# or: conda env create -f environment.yml && conda activate ctdproc
# (environment.yml already runs both pip steps above)
```

Then run `pytest tests/`, just to check it actually works.

This installs the `ctdproc` command (`process`/`align`/`celltm`/`slope` subcommands,
each taking a config path; `--data-dir`/`--output-dir` override the config's own
`constants.data_dir`/`output_dir`). `ctdproc --help` lists them all.

---

## Quick start

1. Put the raw `.hex` + `.XMLCON` pair in `data/`, same base name (e.g.
   `MIXSED2_001.hex` + `MIXSED2_001.XMLCON`).
2. Minimal `proc/config.yaml`, just to decode and convert one cast, no
   corrections yet:

```yaml
constants:
  sample_interval: 1/24
  name: "MIXSED2"
  ind: [1, 1]          # just cast 001, to start
  convert: 'yes'
  time_ref: 'System UTC'

features: []           # add real correction steps once you have fitted
                        # coefficients - see Diagnostic finders below
```

3. Run it:
```bash
cd proc
ctdproc process config.yaml
```

4. Check `proc/MIXSED2_001_24hz.cnv`: Sea-Bird-style header, then P/T/T2/C/C2
   at 24 Hz. No `sal00`/`sal11` yet - salinity needs `celltm` or
   `slope_corr` to have run first.

From here, add one correction step at a time. Each one needs real fitted
coefficients from one of the three finders below, not a guessed number.

---

## Running the pipeline

```text
data/ (raw .hex/.XMLCON)  +  proc/config.yaml  →  ctdproc process config.yaml  (run from proc/)
```

```yaml
constants:
  sample_interval: 1/24
  name: "MIXSED2"
  ind: [30, 38]          # cast range -> name_030.hex ... name_038.hex
  convert: 'yes'
  time_ref: 'System UTC'

features:                 # only the uncommented steps run, in this order
  # - name: "align"        {variables, offset}            # from ctdalign_finder
  # - name: "wild_edit"    {variables, std_pass_1, std_pass_2, scans_per_block, distance_to_mean}
  # - name: "low_filter"   {variables, time_constant}
  # - name: "celltm"       {variables, amplitude, time_constant}  # from cellTM_finder
  # - name: "slope_corr"   {variables, slope}             # from slopecorrection_finder
  # - name: "loop_edit"    # NOT for caldip casts - flags bottle-stops as ship-roll noise
  # - name: "bin"          {bin_type, bin_size, type_profile}
```

- `slope_corr` has to come after `celltm`.
- `.cnv` output only carries P/T/C/salinity right now.

---

## Diagnostic finders

Each one fits the coefficients for one `features:` step above. Run from
`proc/`, in this order: **align → celltm → slope**.

| Finder | Fits | Config key | Run | Output |
|---|---|---|---|---|
| `ctdalign_finder` | sensor time-lag | `alignment_settings` | `ctdproc align config_align.yaml` | `alignment_report.csv`, paste straight into `align`'s `offset:` |
| `cellTM_finder` | thermal-mass α/τ | `celltm_settings` | `ctdproc celltm config_celltm.yaml` | `alpha_tau_report.csv` + contour plots. Check `edge_pinned` first - if a fit landed right on the search grid's edge (α 0.01–0.09, τ 1–16), the real optimum is outside it |
| `slopecorrection_finder` | conductivity slope | `slope_settings` | `ctdproc slope config_slopecorr.yaml` | `slope_report.csv` + ratio plots. Iterative 3σ outlier rejection |

Example `slope_settings`:
```yaml
slope_settings:
  bottle_sal_file: "Bottle_Salinity.csv"   # columns: Station, No_bottle, Sal_avg
  scan_offset: [2, 2]        # seconds before bottle closure
  scan_duration: [2, 2]
  temperature_sensors: ["temperature", "temperature2"]
  conductivity_sensors: ["conductivity", "conductivity2"]
```
(`[2, 2]` is the GO-SHIP standard.)

`bottle_sal_file` itself is just a plain CSV, one row per bottle:
```text
Station,No_bottle,Sal_avg
MIXSED2_044,6.0,34.7119
MIXSED2_045,9.0,34.7166
```

---

## Known gaps

- `.cnv` output skips oxygen/chlorophyll/turbidity/PAR. These are already
  parsed and can be converted from the XMLCON, just not written into the
  `.cnv` yet.
- Missing conversion for:
  `UVP6`, `pH_Sensor`, `WET_LabsCStar`, and `FluoroSeatechWetlabsFLF_Sensor`.
- `ctdalign_finder` only resolves lag in whole multiples of the sample interval
  (e.g. ~0.042 s at 24 Hz) - nothing in between.
- `cellTM_finder`'s search grid (α 0.01–0.09, τ 1–16) is fixed, same for
  every cast and sensor, not something you can set per campaign.
- `slopecorrection_finder` and `cellTM_finder` need improvement for outliers detection routines
- The vendored `seabirdscientific/` has one local patch: latin-1 decoding
  in `instrument_data.py`. If your cruise's metadata (ship name, PI, etc.)
  is plain ASCII, you can `pip install seabirdscientific` straight over it
  with no issue.

