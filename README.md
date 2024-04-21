# online-store-sku-monitor

## introduction
- Monitor stock of new tech products and alert on found items
- Stores and SKUs are configured in `src/data.yaml`
- A few control variables can be configured in `src/config.yaml` for controlling looping and logging behaviour

## usage

Run using make:

```bash
make run
```

# voice alert

Voice alerts are configured using `pyttsx3` and will be enabled if a compatible engine backend is available.
