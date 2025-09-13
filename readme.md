# Mag-SpeedTest CLI Tool

A Python command-line tool to run internet speed tests using `speedtest-cli`, filter servers by country and city, and select the best performing server based on download or upload speed. Results are displayed in a clean tabular format with color highlighting and saved to CSV for later analysis.

## Features
- Test internet speed from multiple servers in a given country.
- Filter by specific cities.
- Limit the number of results with `--limit`.
- Choose the best server based on:
  - Download speed (`--optimalDownload`)
  - Upload speed (`--optimalUpload`)
  - Balanced (default).
- Save results automatically to `speedtest_results.csv`.
- Colorized and aligned output for easy readability.

## Installation
```bash
git clone https://github.com/yourusername/speedtest-cli-tool.git
cd speedtest-cli-tool
pip install -r requirements.txt
````


## Usage

Run with defaults (tests servers in Pakistan):

```bash
python main.py
```

Limit to top 3 servers in Lahore:

```bash
python main.py --country Pakistan --cities Lahore --limit 3
```

Pick best server by **download speed**:

```bash
python main.py --optimalDownload
```

Pick best server by **upload speed**:

```bash
python main.py --optimalUpload
```

## Output Example

```
City Name       Sponsor                        Country          Hostname                   Download      Upload
Lahore          EarthLink Broadband            Pakistan         ookla.elb.com.pk:8080      8.72 Mbps     10.73 Mbps

🏆 Best Server: EarthLink Broadband (Lahore, Pakistan)
  - Download: 8.72 Mbps | Upload: 10.73 Mbps

✅ Results saved to speedtest_results.csv
```

---

📊 Use it to benchmark your network and log historical data for comparison.
