import speedtest
import csv
import json
import argparse
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

# CSV file to save results
OUTPUT_FILE = "speedtest_results.csv"


def list_servers():
    """List all available servers with colorized headers and aligned columns."""
    st = speedtest.Speedtest(secure=True)
    st.get_servers()
    servers = st.servers

    # Print header
    print(
        f"{Fore.CYAN}{'City Name':<20}{Style.RESET_ALL}  "
        f"{Fore.YELLOW}{'Sponsor':<30}{Style.RESET_ALL}  "
        f"{Fore.GREEN}{'Country':<20}{Style.RESET_ALL}  "
        f"{Fore.MAGENTA}{'Hostname':<35}{Style.RESET_ALL}"
    )

    for server_list in servers.values():
        for server in server_list:
            print(
                f"{server['name'][:20]:<20}  "
                f"{server['sponsor'][:30]:<30}  "
                f"{server['country'][:20]:<20}  "
                f"{server['host'][:35]:<35}"
            )


def run_speedtest(target_country="Pakistan", target_cities=None, limit=5):
    st = speedtest.Speedtest(secure=True)
    st.get_servers()
    servers = st.servers
    results = []
    city_servers = []

    # If no cities provided, test all servers in country
    if target_cities:
        for city in target_cities:
            for server_list in servers.values():
                for server in server_list:
                    if city.lower() in server["name"].lower() and server["country"].lower() == target_country.lower():
                        city_servers.append((city, server))
    else:
        # Use actual server["name"] instead of faking it as city
        for server_list in servers.values():
            for server in server_list:
                if server["country"].lower() == target_country.lower():
                    city_servers.append((server["name"], server))  # <-- keep server name


    if not city_servers:
        print(f"⚠️ No servers found in {target_country} for given cities.")
        return []

    # Print header
    print(
        f"{Fore.CYAN}{'City Name':<15}{Style.RESET_ALL}  "
        f"{Fore.YELLOW}{'Sponsor':<30}{Style.RESET_ALL}  "
        f"{Fore.GREEN}{'Country':<15}{Style.RESET_ALL}  "
        f"{Fore.MAGENTA}{'Hostname':<25}{Style.RESET_ALL}  "
        f"{Fore.RED}{'Download':<12}{Style.RESET_ALL}  "
        f"{Fore.BLUE}{'Upload':<12}{Style.RESET_ALL}"
    )

    for cindex, (city, server) in enumerate(city_servers[:limit], start=1):
        st.get_best_server([server])

        # Run test
        download = st.download() / 1_000_000
        upload = st.upload() / 1_000_000
        ping = st.results.ping

        print(
            f"{city[:15]:<15}  "
            f"{server['sponsor'][:30]:<30}  "
            f"{server['country'][:15]:<15}  "
            f"{server['host'][:25]:<25}  "
            f"{download:<12.2f}  "
            f"{upload:<12.2f}"
        )

        results.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "city": city,
            "sponsor": server["sponsor"],
            "server": server["name"],
            "ping_ms": round(ping, 2),
            "download_mbps": round(download, 2),
            "upload_mbps": round(upload, 2),
        })

    return results


def select_best_server(results, optimal_download=False, optimal_upload=False):
    if not results:
        return None

    if optimal_download:
        best = max(results, key=lambda r: r["download_mbps"])
    elif optimal_upload:
        best = max(results, key=lambda r: r["upload_mbps"])
    else:
        # default: balance of download + upload
        best = max(results, key=lambda r: (r["download_mbps"], r["upload_mbps"]))

    print(
        f"\n🏆 Best Server: {best['server']} ({best['city']}, {best['sponsor']})\n"
        f"  - Download: {best['download_mbps']} Mbps | Upload: {best['upload_mbps']} Mbps"
    )
    return best


def save_results(results):
    fieldnames = ["timestamp", "city", "sponsor", "server", "ping_ms", "download_mbps", "upload_mbps"]

    try:
        with open(OUTPUT_FILE, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if f.tell() == 0:
                writer.writeheader()
            writer.writerows(results)
        print(f"\n✅ Results saved to {OUTPUT_FILE}")
    except Exception as e:
        print(f"Error saving results: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Speedtest and pick best server")
    parser.add_argument("--country", type=str, default="Pakistan", help="Country to search servers in")
    parser.add_argument("--cities", nargs="*", help="Optional list of city names")
    parser.add_argument("--optimalDownload", action="store_true", help="Pick best server by download speed")
    parser.add_argument("--optimalUpload", action="store_true", help="Pick best server by upload speed")
    parser.add_argument("--limit", default=5, help="Limit Output Results")
    parser.add_argument("--servers", action="store_true", help="List all available servers")
    args = parser.parse_args()

    if args.servers:
        list_servers()
    else:
        results = run_speedtest(target_country=args.country, target_cities=args.cities, limit=int(args.limit))
        if results:
            best = select_best_server(results, args.optimalDownload, args.optimalUpload)
            save_results(results)
