#!/bin/bash

yt map-reduce \
    --mapper 'python3 run.py' \
    --reducer 'python3 aggregate.py' \
    --src //home/maps_mrc/dasimagin/games \
    --dst //home/maps_mrc/dasimagin/result \
    --format json \
    --reduce-by 'name' \
    --spec '{
        pool_trees=[gpu_tesla_v100];
        map_job_count=2;
        mapper={
            layer_paths=["//home/maps_mrc/porto_layers/xenial_python-3_dl.tar.xz"];
            local_files=[
                run.py;agent.py;backend.py;renju.py;
                dummy.py
            ];
        };
        reducer={
            local_files=[
                aggregate.py
            ]
        };
    }'
