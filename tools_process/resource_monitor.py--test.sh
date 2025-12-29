# test local python
python3 resource_monitor.py --output resource_view.png python3 -c "a = sum([i*i for i in range((10**8)*3)]); print('test', a)"
python3 resource_monitor.py --output resource_view.png --snapshot-interval 2 python3 -c "a = sum([i*i for i in range((10**8)*3)]); print('test', a)"
# test docker
python3 resource_monitor.py --output resource_view.png docker run --rm -it hictools/gothic:1.44.0  python3 -c "a = sum([i*i for i in range((10**8)*3)]); print('test', a)"
# test plot data
python3 resource_monitor.py --plot-data resource_view.json
