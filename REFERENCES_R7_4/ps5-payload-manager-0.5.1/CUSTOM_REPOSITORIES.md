# Custom Payload Repositories

PS5 Payload Manager supports adding custom, third-party payload repositories (sources) in addition to the default official repository. This allows developers and communities to host and distribute their own payloads.

---

## JSON Format Specification

To create a repository, you must host a JSON file that conforms to the following schema.

### Core Rules:
1. The JSON must contain a top-level `"name"` field.
2. The `"name"` field **must appear before** the `"payloads"` field in the JSON structure so the parser can locate it correctly.
3. The `"payloads"` field must be an array of payload objects.

### Example JSON:
```json
{
  "name": "My Custom Payloads",
  "payloads": [
    {
      "name": "FTP Server",
      "filename": "ftpsrv_v0.19.elf",
      "url": "https://example.com/payloads/ftpsrv_v0.19.elf",
      "description": "A simple FTP server that accepts connections on port 2121",
      "version": "v0.19",
      "category": "Networking",
      "checksum": "e6c1babbfd5e1b766d12b659853b514b9faedf6333cbe8cb514b1a3e79b7ce39"
    },
    {
      "name": "Debug Tool",
      "filename": "debug_tool.elf",
      "url": "https://example.com/payloads/debug_tool.elf",
      "description": "A helper utility to dump debug information.",
      "version": "v1.0"
    }
  ]
}
```

### Field Reference:

| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| **`name`** (top-level) | String | Yes | The display name of your repository catalog in the user interface (e.g. `"My Custom Payloads"`). |
| **`payloads`** (top-level) | Array | Yes | List of payload items available in this repository. |
| **`name`** (item-level) | String | Yes | Human-readable name of the specific payload. |
| **`filename`** (item-level) | String | Yes | The exact filename (including extension like `.elf`, `.bin`, `.lua`) when saved. |
| **`url`** (item-level) | String | Yes | Direct HTTP or HTTPS link where the payload binary can be downloaded. |
| **`description`** (item-level) | String | No | A description of what the payload does, displayed in the dashboard. |
| **`version`** (item-level) | String | No | Version string used for update checks (e.g. `"v1.0"`). |
| **`category`** (item-level) | String | No | The category name used to group payloads in the frontend (e.g. `"Networking"`). Defaults to `"Uncategorized"`. |
| **`checksum`** (item-level) | String | No | **SHA-256** hash (64 hex characters) of the file. If provided, the manager automatically validates the downloaded file against it before installation. |

---

## Hosting Your Repository

1. **Accessibility**: Upload your JSON file and your payload binaries to any static hosting provider (e.g., GitHub Pages, Vercel, Netlify, or your own VPS). The PS5 must be able to resolve and reach the host IP.
2. **CORS Headers**: To ensure that the web interface can interact with the files from the browser, your server should respond with CORS headers:
   ```http
   Access-Control-Allow-Origin: *
   ```

---

## Adding the Source in Payload Manager

1. Open the Payload Manager dashboard.
2. Navigate to **Settings** (gear icon) and select **Manage Sources**.
3. Click **Add Source**, paste the direct HTTP/HTTPS URL to your `payloads.json` file, and press **Add**.
4. The dashboard will validate the source and add it to your catalog list.
