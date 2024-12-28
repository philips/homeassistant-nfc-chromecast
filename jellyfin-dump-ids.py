import argparse
import requests

def get_show_id(base_url, api_key, library_id, show_name):
    """Finds the show ID within a library."""
    url = f"{base_url}/Items?ParentId={library_id}&Recursive=true&IncludeItemTypes=Series"
    headers = {"X-Emby-Token": api_key}
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception for bad status codes

    for item in response.json()['Items']:
        if item['Name'] == show_name:
            return item['Id']
    return None

def get_episode_ids(base_url, api_key, show_id):
    """Retrieves a list of episode IDs for a given show."""
    url = f"{base_url}/Items?ParentId={show_id}&Recursive=true"
    headers = {"X-Emby-Token": api_key}
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    episode_ids = []
    for item in response.json()['Items']:
        if item['Type'] == 'Episode':
            episode_ids.append(item['Id'])
    return episode_ids

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get episode IDs from Jellyfin")
    parser.add_argument("--base-url", help="Jellyfin server URL", required=True)
    parser.add_argument("--api-key", help="Jellyfin API key", required=True)
    parser.add_argument("--library-id", help="Jellyfin library ID", required=True)
    parser.add_argument("--show-name", help="Name of the show", required=True)
    args = parser.parse_args()

    show_id = get_show_id(args.base_url, args.api_key, args.library_id, args.show_name)
    if show_id:
        episode_ids = get_episode_ids(args.base_url, args.api_key, show_id)
        for item in episode_ids:
            print('- ' + item)
    else:
        print(f"Show '{args.show_name}' not found.")
