# stockmonitor
- Monitor stock of new tech products and alert on found items
- Items are configured in stockmonitor/src/vendors/${vendor-name}/items.json
- Individual vendors can be disabled in stockmonitor.py by commenting them out
- There are also a few boolean flags in stockmonitor.py for controlling looping and logging behaviour
- Run from src:
```bash
cd stockmonitor/src
python3 ./stockmonitor.py
```
