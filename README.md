# photo-geo-locator

**Extract GPS data from JPEG files in the `assets` directory.**
```sh
python3 src/gps_extractor.py
```

**Plot pins on a map and save it to the `exports` directory.**
```sh
python3 src/map_plotter.py
```

---

```sh
# Build and Start Container
docker compose up -d --build

# Access the Container
docker compose exec app /bin/bash

# Stop and Remove Container
docker compose down
```
